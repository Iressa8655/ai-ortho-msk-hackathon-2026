"""把 vault 的 Submission review 頁面組回 repo 的三份英文 markdown，
然後做 PDF 和 zip 的 v2。

只取每頁 <!-- EN START --> 到 <!-- EN END --> 之間的英文，
callout 和中文不會進去。頁面順序照檔名的 S01、C01、B01 排。
"""

import os
import re
import subprocess
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VAULT = Path(r"C:\Users\User\Dropbox\Iressa's note\Projects"
             r"\AI in Orthopaedics Hackathon 2026\Submission review")
PANDOC = r"C:\Users\User\AppData\Local\Pandoc\pandoc.exe"
XELATEX_DIR = r"C:\Users\User\AppData\Local\Programs\MiKTeX\miktex\bin\x64"

TARGETS = {
    "S": REPO / "SUBMISSION.md",
    "M": REPO / "medicine" / "clinical_implementation.md",
    "T": REPO / "technical" / "technical_report.md",
    "B": REPO / "business" / "business_case.md",
}
MARKERS = {"S": "# ", "M": "## ", "T": "## ", "B": "## "}


def read_head(path, marker):
    """保留原檔第一個節標題之前的檔頭（YAML 或 H1 加前言）。"""
    text = path.read_text(encoding="utf-8")
    return re.split(r"^(?=" + re.escape(marker) + r"(?!#))", text, flags=re.M)[0]


IMAGE_DIRS = ["business", "technical/figures", "medicine"]


def repo_image_path(name):
    """vault 的 ![[x.jpg]] 轉成 repo 相對路徑，給 pandoc 用。找不到就原樣回傳。"""
    for folder in IMAGE_DIRS:
        if (REPO / folder / name).exists():
            return f"{folder}/{name}"
    print("warning: image not found in repo:", name)
    return name


def convert_wikilink_images(text):
    """![[fig.jpg|caption]] → ![caption](business/fig.jpg)，Obsidian 和 pandoc 兩邊都能看。"""
    pattern = r"!\[\[([^\]|]+\.(?:jpg|jpeg|png|svg))(?:\|([^\]]*))?\]\]"

    def repl(match):
        name, caption = match.group(1).strip(), match.group(2) or ""
        return f"![{caption}]({repo_image_path(name)})"

    return re.sub(pattern, repl, text)


def extract_english(page):
    text = page.read_text(encoding="utf-8")
    match = re.search(
        r"(?:<!-- EN START -->|%% EN START %%)\n(.*?)(?:<!-- EN END -->|%% EN END %%)",
        text, re.S)
    if not match:
        raise SystemExit(f"no EN block in {page.name}")
    english = strip_callouts(match.group(1))
    english = strip_her_comments(english, page.name)
    return convert_wikilink_images(english.rstrip()) + "\n\n"


def strip_her_comments(text, page_name):
    """拿掉她的行內批註，::像這樣:: 和 %%像這樣%%，剩下還有中文就警告。"""
    text = re.sub(r"::.*?::", "", text, flags=re.S)
    text = re.sub(r"%%.*?%%", "", text, flags=re.S)
    text = re.sub(r"[ \t]{2,}", " ", text)
    for line in text.split("\n"):
        if re.search(r"[一-鿿]", line):
            print(f"warning: Chinese left in EN block of {page_name}: {line[:80]}")
    return text


def strip_callouts(text):
    """拿掉英文區塊裡的 Obsidian callout（> [!...] 開頭的整個引用塊）。

    她要逐句建議放在句子旁邊，所以建議 callout 可以放在英文區塊裡，
    組 PDF 時在這裡剝掉，不會進評審看的版本。
    """
    kept, skipping = [], False
    for line in text.split("\n"):
        if line.startswith("> [!"):
            skipping = True
            continue
        if skipping and line.startswith(">"):
            continue
        skipping = False
        kept.append(line)
    return "\n".join(kept)


def number_figures(texts):
    """依 pandoc 的輸出順序把 {fig:檔名} 換成圖號。

    pandoc 自己會在圖說前面加 Figure N，所以這裡只負責讓內文的
    「(Figure {fig:x.jpg})」變成同一個 N。
    """
    order = []
    for text in texts:
        for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
            name = os.path.basename(match.group(1))
            if name not in order:
                order.append(name)
    numbers = {name: i + 1 for i, name in enumerate(order)}

    def repl(match):
        name = match.group(1).strip()
        if name not in numbers:
            print("warning: figure reference to unknown image:", name)
            return "?"
        return str(numbers[name])

    return [re.sub(r"\{fig:([^}]+)\}", repl, text) for text in texts]


# Business case 照 HM Treasury Green Book 的五格排，每格一個 Part 標題，
# 節號不改（內文的 section N 互相參照才不會壞），節標題降成 ###。
FIVE_CASES = [
    ("Part A. Strategic case: the problem, the solution, and why now",
     "The case for change. Sarcoma subtype decides the operation and the oncology plan, "
     "the confirming genomic test is centralised and slow, and a wrong first order costs a "
     "full test cycle in England and the single reimbursed test in Taiwan. We propose "
     "decision support that reads the H&E slide already in hand and makes the first "
     "genomic order the right one. This part states the problem, the solution, and what the "
     "submitted prototype does and does not prove.",
     ["B01", "B02", "B03"]),
    ("Part B. Economic case: what it saves and what it costs to run",
     "Value for money. The direct laboratory saving is modest because the test is cheap; the "
     "value is in patient-days of waiting removed and operations planned with the subtype known. "
     "Inference cost per slide is negligible, so the cost of the service is validation, "
     "regulation and support. Every input is labelled sourced or assumption and can be changed "
     "in the savings notebook.",
     ["B04", "B05"]),
    ("Part C. Commercial case: who buys, how they pay, and who else sells",
     "The buyer and the deal. One payer in each country, NHS England through the Genomic "
     "Laboratory Hubs and the National Health Insurance Administration in Taiwan, and two kinds "
     "of user who pay nothing extra. The product reaches them inside the digital pathology "
     "viewer they already use. No company sells an H&E-to-fusion product for sarcoma today.",
     ["B06", "B07", "B08", "B09"]),
    ("Part D. Financial case: budget and funders",
     "Affordability. Three years from prototype to first licence, grant-funded so that the "
     "first contract is signed with evidence rather than a price guess. The budget is itemised "
     "line by line and each line is marked sourced or assumption. The first application is the "
     "Cancer Research UK Early Detection and Diagnosis Primer Award.",
     ["B10", "B11", "B12"]),
    ("Part E. Management case: delivery, regulation, team and risks",
     "Deliverability. Research use, then shadow deployment at one hub, then regulated use as "
     "UKCA-marked Class IIa decision support that a pathologist confirms. Performance is reported "
     "by laboratory, scanner and population, and the single largest risk, a model that learns "
     "stain colour instead of biology, has a measured gate before any clinical use.",
     ["B13", "B14", "B15", "B16", "B17", "B18"]),
]


def page_for(key):
    hits = sorted(VAULT.glob(f"{key} [A-E]. *.md")) or sorted(VAULT.glob(f"{key} *.md"))
    if not hits:
        raise SystemExit(f"missing page for {key}")
    return hits[0]


# 內文裡提到的節號是 vault 頁的舊號，組 PDF 時換成新號。只列有出現的。
REF_FIXES = []  # 2026-10-07 B 頁已改名重編，不再需要


def assemble_business_case():
    parts = []
    number = 0
    listed = {k for _, _, keys in FIVE_CASES for k in keys}
    unlisted = [p.name for p in VAULT.glob("B[0-9][0-9] *.md") if p.name[:3] not in listed]
    if unlisted:
        print("warning: B pages not placed in any case:", unlisted)
    for title, lead, keys in FIVE_CASES:
        parts.append(f"## {title}\n\n{lead}\n\n")
        for key in keys:
            number += 1
            english = extract_english(page_for(key))
            # 「## 6. Title」→「### 6. Title」，頁名已經照 PDF 編號
            english = re.sub(r"^## \d+\. ", f"### {number}. ", english, count=1, flags=re.M)
            for page, old, new in REF_FIXES:
                if page == key:
                    if old not in english:
                        print(f"warning: ref fix not found in {key}: {old}")
                    english = english.replace(old, new)
            parts.append(english)
    return "".join(parts)


def assemble():
    assembled = {}
    for prefix, target in TARGETS.items():
        pages = sorted(VAULT.glob(f"{prefix}[0-9][0-9] *.md"))
        if not pages:
            continue
        if prefix == "B":
            body = assemble_business_case()
        else:
            body = "".join(extract_english(p) for p in pages)
        assembled[prefix] = read_head(target, MARKERS[prefix]) + body
        print(f"{target.relative_to(REPO)}: {len(pages)} sections")
    # 圖號照 pandoc 讀檔順序 S → M → T → B
    keys = [k for k in TARGETS if k in assembled]
    numbered = number_figures([assembled[k] for k in keys])
    for key, text in zip(keys, numbered):
        TARGETS[key].write_text(text, encoding="utf-8")


def build_pdf():
    env = dict(os.environ)
    env["PATH"] = XELATEX_DIR + os.pathsep + env["PATH"]
    out = REPO / "submission_document_v2.pdf"
    cmd = [
        PANDOC, str(TARGETS["S"]), str(TARGETS["M"]), str(TARGETS["T"]),
        str(TARGETS["B"]),
        "-o", str(out), "--pdf-engine=xelatex",
        "-V", "mainfont=Segoe UI", "-V", "geometry:margin=2cm", "--toc",
    ]
    subprocess.run(cmd, check=True, cwd=REPO, env=env)
    print("pdf", out.name)
    return out


def build_zip(pdf):
    files = [
        "SUBMISSION.md",
        "technical/01_sarcoma_hne_triage.ipynb",
        "technical/02_savings_model.ipynb",
        "technical/03_robustness_checks.ipynb",
        "technical/build_robustness_notebook.py",
        "technical/technical_report.md",
        "technical/requirements.txt",
        "technical/fetch_overviews.py",
        "technical/build_notebook.py",
        "technical/build_savings_notebook.py",
        "technical/data/cohort.csv",
        "technical/data/tcga_sarc_slides_all.csv",
        "technical/data/cohort_with_predictions.csv",
        "medicine/clinical_implementation.md",
        "business/business_case.md",
        "group-member-contact/README.md",
    ]
    files += ["demo/README.md"]  # demo itself is live on Hugging Face; README carries the URL
    out = REPO / "submission_attachments_v2.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(pdf, "submission_document.pdf")
        for f in files:
            if (REPO / f).exists():
                archive.write(REPO / f, f)
    print("zip", out.name, round(out.stat().st_size / 1e6, 1), "MB")


if __name__ == "__main__":
    assemble()
    build_zip(build_pdf())
