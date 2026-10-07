"""從 GDC 只抓 TCGA-SARC 切片的最低解析度層，存成 PNG。

為什麼不抓整張：一張 SVS 動輒 0.5 到 2 GB，這台電腦下載速度約
0.4 MB/s，60 張要好幾天。SVS 是金字塔 TIFF，最低那層只有幾 MB，
用 HTTP Range 只讀那一層，一張約 30 秒。

Notebook 01 會呼叫這裡的函式，已存在的檔案直接跳過。
"""

import time
from pathlib import Path

import fsspec
import pandas as pd
import requests
import tifffile
from PIL import Image
from tqdm import tqdm

GDC_FILES = "https://api.gdc.cancer.gov/files"
GDC_DATA = "https://api.gdc.cancer.gov/data/"
CLASSES = {
    "Leiomyosarcoma, NOS": "LMS",
    "Dedifferentiated liposarcoma": "DDLPS",
}


def list_sarc_slides():
    """向 GDC 要 TCGA-SARC 全部診斷切片的清單，回傳 DataFrame。

    :return: 每列一張切片，含 file_id、file_size、case、diagnosis
    :rtype: pandas.DataFrame
    """
    filters = {
        "op": "and",
        "content": [
            {"op": "=", "content": {
                "field": "cases.project.project_id", "value": "TCGA-SARC"}},
            {"op": "=", "content": {
                "field": "data_type", "value": "Slide Image"}},
            {"op": "=", "content": {
                "field": "experimental_strategy",
                "value": "Diagnostic Slide"}},
        ],
    }
    payload = {
        "filters": filters,
        "fields": ("file_id,file_name,file_size,cases.submitter_id,"
                   "cases.diagnoses.primary_diagnosis"),
        "size": 1000,
        "format": "JSON",
    }
    response = requests.post(GDC_FILES, json=payload, timeout=120)
    response.raise_for_status()
    rows = []
    for hit in response.json()["data"]["hits"]:
        case = hit["cases"][0]
        # 第一個 diagnosis 是原發腫瘤，後面的是第二癌症，只取第一個
        diagnosis = case["diagnoses"][0]["primary_diagnosis"]
        rows.append({
            "file_id": hit["file_id"],
            "file_name": hit["file_name"],
            "file_size_mb": hit["file_size"] / 1e6,
            "case": case["submitter_id"],
            "diagnosis": diagnosis,
        })
    return pd.DataFrame(rows)


def pick_cohort(slides, per_class=30, seed=0):
    """每個病人只留一張（最小的），每類取檔案最小的 per_class 張。

    小檔優先不是偷懶，是因為最低層的大小跟整檔大小成正比，
    小檔的 overview 讀得快。這會帶來一點偏差，notebook 的
    限制那節有講。

    :param slides: list_sarc_slides() 的輸出
    :param per_class: 每類幾個病人
    :return: 篩過的 DataFrame，多一欄 label
    """
    subset = slides[slides["diagnosis"].isin(CLASSES)].copy()
    subset["label"] = subset["diagnosis"].map(CLASSES)
    subset = subset.sort_values("file_size_mb")
    one_per_case = subset.drop_duplicates("case", keep="first")
    cohort = (
        one_per_case.groupby("label", group_keys=False)
        .head(per_class)
        .reset_index(drop=True)
    )
    return cohort


def read_level(file_id, level_from_end=1, block_size=2 * 1024 * 1024):
    """用 HTTP Range 只讀 SVS 金字塔的某一層，從最低解析度往上數。

    :param file_id: GDC file uuid
    :param level_from_end: 1 是最低層（幾 MB），2 是上一層（約 16 倍像素）
    :return: RGB numpy array
    """
    filesystem = fsspec.filesystem("http", block_size=block_size)
    with filesystem.open(GDC_DATA + file_id, "rb") as handle:
        tiff = tifffile.TiffFile(handle)
        level = tiff.series[0].levels[-level_from_end]
        return level.asarray()


def read_lowest_level(file_id, block_size=2 * 1024 * 1024):
    """最低解析度層，notebook 01 用的，等於 read_level(..., 1)。"""
    return read_level(file_id, 1, block_size)


def fetch_cohort(cohort, out_dir, level_from_end=1):
    """把 cohort 每張切片的某一層存成 PNG，已存在的跳過。

    :param cohort: pick_cohort() 的輸出
    :param out_dir: PNG 存放資料夾
    :param level_from_end: 1 最低層，2 上一層
    :return: 多一欄 png 路徑的 DataFrame
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for _, row in tqdm(cohort.iterrows(), total=len(cohort),
                       desc="fetch overviews"):
        target = out_dir / f"{row['case']}_{row['label']}.png"
        if not target.exists():
            # 網路偶爾斷線（DNS 失敗），最多重試 5 次再放棄
            for attempt in range(5):
                try:
                    array = read_level(row["file_id"], level_from_end)
                    Image.fromarray(array).save(target)
                    break
                except Exception as error:      # noqa: BLE001
                    print(f"retry {attempt + 1} for {row['case']}: {error}")
                    time.sleep(20)
        paths.append(str(target))
    cohort = cohort.copy()
    cohort["png"] = paths
    return cohort


if __name__ == "__main__":
    here = Path(__file__).parent
    slides = list_sarc_slides()
    slides.to_csv(here / "data" / "tcga_sarc_slides_all.csv", index=False)
    cohort = pick_cohort(slides)
    cohort = fetch_cohort(cohort, here / "data" / "overviews")
    cohort.to_csv(here / "data" / "cohort.csv", index=False)
    print(cohort["label"].value_counts())
