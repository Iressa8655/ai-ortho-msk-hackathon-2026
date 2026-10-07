"""把 submission 的三份英文 markdown 拆成一節一頁，寫進 vault 的 Submission review。

每頁：frontmatter、中文一句話、review 鷹架、然後英文原文夾在
<!-- EN START --> 與 <!-- EN END --> 之間。她改英文就改那一段，
assemble_from_vault.py 會把它組回 repo 再做 PDF。

已存在的頁面不覆蓋，避免蓋掉她改過的字。
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VAULT = Path(r"C:\Users\User\Dropbox\Iressa's note\Projects"
             r"\AI in Orthopaedics Hackathon 2026\Submission review")

# SUBMISSION.md 的節是 H1（# 1. Summary），另外兩份是 H2
SOURCES = [
    ("S", REPO / "SUBMISSION.md", "# "),
    ("C", REPO / "medicine" / "clinical_implementation.md", "## "),
    ("B", REPO / "business" / "business_case.md", "## "),
    ("P", REPO / "business" / "sba_business_plan.md", "## "),
]

# 每節一句中文，讓她不用先讀英文就知道這節在講什麼
GIST = {
    "S1": "一頁摘要，問題、解法、效率槓桿、附件清單。評審第一眼看的。",
    "S2": "Baseline 結果，60 人 AUC 0.82，哪裡錯、限制。",
    "S3": "付款路徑那張 BioRender 圖。",
    "S4": "怎麼重跑，評審照這個做。",
    "S5": "成員與貢獻，現在只有妳。",
    "C1": "臨床問題，sarcoma 診斷路徑五步，時間卡在轉診和基因檢測。",
    "C2": "AI 放在第 2 步和第 3 步之間，先決定送哪種檢測。",
    "C3": "四階段導入，回溯 → 影子 → 顧問 → 轉診分流，每階段有指標。",
    "C4": "怎麼接進現有系統，切片不出實驗室。",
    "C5": "安全設計，醫師先看片、可棄權、記錄版本。",
    "C6": "台灣版本，健保一生一次。",
    "C7": "多元與公平，亞洲族群一開始就在驗證集。",
    "B1": "我們解決什麼問題，附來源。",
    "B2": "解法一段，效率槓桿一句。",
    "B3": "誰付錢，五種買家。",
    "B4": "付款路徑圖的文字版。",
    "B5": "三年上市路線。",
    "B6": "多元與倫理承諾。",
    "B7": "這次交的是什麼、不是什麼。",
    "B8": "省多少錢、為什麼政府付，數字來自 notebook 02。",
    "B9": "倫理與法規六步。",
    "B10": "business plan 目錄總表。",
    "B11": "市場大小，英國 5,900，台灣約 585。",
    "B12": "競爭者，Owkin、Panakeia、Paige，sarcoma 沒人做。",
    "B13": "單位經濟，一張 US$0.08。",
    "B14": "團隊角色，誰在、誰要邀。",
    "B15": "風險與對策。",
    "B16": "里程碑與資金總表。",
    "B17": "一季一個交付的時程。",
    "B18": "三年預算逐行，約 £406k。",
    "B19": "誰在發錢，排過適合度，先申 CRUK primer。",
    "P1": "SBA 執行摘要，使命、產品、為何會成功、團隊、地點。",
    "P2": "SBA 公司描述，問題、優勢、法律結構（spin-out 假設）。",
    "P3": "SBA 市場分析，產業展望、市場大小、競爭者。",
    "P4": "SBA 組織與管理，角色表、結構、顧問委員會。",
    "P5": "SBA 產品線，賣什麼、好處、五階段生命週期、IP。",
    "P6": "SBA 行銷與銷售，誰買、交易怎麼發生、通路、留客。",
    "P7": "SBA 資金需求，£406k、全補助、申請順序。",
    "P8": "SBA 財務預測，誠實的 break-even，每片計價打不平。",
    "P9": "SBA 附件清單。",
}

SCAFFOLD = """
> [!question]- ❓ 評審會問什麼
> ~={red}**YOU FILL IN**=~ 想像 coder、data scientist、clinician、industry 四種評審各問一句。

> [!example]- ✏️ 要改的地方
> - [ ] ~={red}**YOU FILL IN**=~

> [!success]- ✅ 定稿
> - [ ] 這一節看過，英文可以直接用
"""


def split_sections(text, marker):
    """依標題層級切成 (標題, 內容)，第一個標題之前的檔頭另外回傳。

    :param text: 整份 markdown
    :param marker: "# " 或 "## "
    """
    pattern = r"^(?=" + re.escape(marker) + r"(?!#))"
    parts = re.split(pattern, text, flags=re.MULTILINE)
    head = parts[0]
    sections = []
    for part in parts[1:]:
        title_line, _, body = part.partition("\n")
        title = title_line[len(marker):].strip()
        sections.append((title, body.rstrip() + "\n"))
    return head, sections


def page_name(prefix, number, title):
    clean = re.sub(r"^\d+\.\s*", "", title)
    clean = re.sub(r"[\\/:*?\"<>|]", "", clean)
    clean = clean.replace(",", "，")[:60].rstrip()
    return f"{prefix}{number:02d} {clean}.md"


def write_page(target, key, marker, title, body, source):
    content = (
        "---\n"
        f"title: {target.stem}\n"
        "type: submission-review\n"
        f"source_file: {source.relative_to(REPO).as_posix()}\n"
        f"section_key: {key}\n"
        "status: to-review\n"
        "---\n\n"
        f"# {target.stem}\n\n"
        f"**這節在講什麼。** {GIST.get(key, '')}\n\n"
        "**Next action.** 讀下面的英文，把要改的寫進 ✏️，改好的直接改英文那段。/ "
        "全部打勾後跑 `tools/assemble_from_vault.py` 組新版。\n"
        f"{SCAFFOLD}\n"
        "---\n\n"
        "<!-- EN START -->\n"
        f"{marker}{title}\n\n{body}"
        "<!-- EN END -->\n"
    )
    target.write_text(content, encoding="utf-8")


def write_index(rows):
    lines = [
        "---", "title: 00 Review index", "type: index",
        "date: 2026-10-01", "---", "",
        "# 00 Review index，一節一頁，改完組回 PDF",
        "",
        ("**Next action.** 從 S01 開始，一頁一頁看，每頁三個 callout 填完打勾。/ "
        "全部打勾後說一聲，我跑 `assemble_from_vault.py` 出 v2 PDF 和 zip。"),
        "",
        ("新截止 **2026-10-08**。/ 英文原文夾在每頁的 `<!-- EN START -->` 到 "
        "`<!-- EN END -->` 之間，改那一段就會進 PDF，callout 不會。"),
        "",
        "| # | 頁 | 來源檔 | 看過 |",
        "|---|---|---|---|",
    ]
    for key, name, src in rows:
        lines.append(f"| {key} | [[{name}]] | `{src.as_posix()}` | ☐ |")
    lines += [
        "",
        "## 怎麼組回去",
        "",
        "```bash",
        ("C:/Users/User/miniconda3/envs/spatial/python.exe "
        "C:/Users/User/Documents/GitHub/ai-ortho-msk-hackathon-2026/tools/assemble_from_vault.py"),
        "```",
        "",
        "產出 `submission_document_v2.pdf` 和 `submission_attachments_v2.zip`。",
    ]
    (VAULT / "00 Review index.md").write_text("\n".join(lines) + "\n",
                                              encoding="utf-8")


def main():
    VAULT.mkdir(parents=True, exist_ok=True)
    index_rows = []
    for prefix, source, marker in SOURCES:
        _, sections = split_sections(source.read_text(encoding="utf-8"), marker)
        for number, (title, body) in enumerate(sections, start=1):
            key = f"{prefix}{number}"
            target = VAULT / page_name(prefix, number, title)
            index_rows.append((key, target.stem, source.relative_to(REPO)))
            if not target.exists():          # 她可能改過，不覆蓋
                write_page(target, key, marker, title, body, source)
    write_index(index_rows)


if __name__ == "__main__":
    main()
    print("review pages written to", VAULT)
