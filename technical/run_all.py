"""一鍵重跑所有 notebook，並印出每張圖和每個資料檔的 MD5，給評審核對。

用法，在 technical/ 裡：

    python run_all.py            # 依序執行 01 到 05，輸出留在 notebook 裡
    python run_all.py --check    # 不執行，只印現有輸出的 MD5

第一次執行會下載約 150 張切片縮圖，之後走快取。
"""

import argparse
import hashlib
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).resolve().parent
NOTEBOOKS = [
    "01_sarcoma_hne_triage.ipynb",
    "02_savings_model.ipynb",
    "03_robustness_checks.ipynb",
    "04_competitor_landscape.ipynb",
    "05_more_data_checks.ipynb",
]
CHECKED = [
    "figures/*.png",
    "data/cohort.csv",
    "data/cohort_with_predictions.csv",
    "data/cohort_random.csv",
    "data/landscape_*.csv",
]


def md5_of(path):
    """回傳檔案內容的 MD5，給評審比對用。"""
    digest = hashlib.md5()
    with open(path, "rb") as handle:
        digest.update(handle.read())
    return digest.hexdigest()


def run_notebook(name):
    """用 nbclient 跑一本 notebook，輸出寫回同一個檔案。"""
    path = HERE / name
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=7200,
        kernel_name="python3",
        resources={"metadata": {"path": str(HERE)}},
    )
    print(f"running {name} ...", flush=True)
    try:
        client.execute()
    finally:
        nbformat.write(notebook, path)
    print(f"done    {name}", flush=True)


def print_checksums():
    """印出所有輸出檔的 MD5，排序固定，方便 diff。"""
    paths = []
    for pattern in CHECKED:
        paths.extend(sorted(HERE.glob(pattern)))
    for path in paths:
        print(f"{md5_of(path)}  {path.relative_to(HERE)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="only print checksums of the existing outputs",
    )
    args = parser.parse_args()
    if not args.check:
        for name in NOTEBOOKS:
            run_notebook(name)
    print_checksums()
    return 0


if __name__ == "__main__":
    sys.exit(main())
