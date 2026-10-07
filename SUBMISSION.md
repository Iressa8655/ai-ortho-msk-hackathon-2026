---
title: "H&E-first molecular triage for sarcoma: a reproducible proof of concept on open data"
subtitle: "AI in Orthopaedics and MSK 2026 Hackathon submission. Executive summary, medical part, technical part, business case"
author: "I-Han Cheng, MD, DPhil student, NDORMS, University of Oxford (team lead, sole member)"
date: "8 October 2026"
geometry: margin=2cm
fontsize: 10pt
colorlinks: true
---

# Executive summary
![Today, the slide waits three weeks and the surgeon guesses between four treatments; with AI triage on day one, the right test is ordered once](business/fig_before_after_ai_triage_biorender.png)

**Problem.** Sarcoma subtype decides the operation and the oncology plan, and many subtypes are defined by a gene fusion. The molecular test that names the fusion is slow and centralised: in England urgent solid tumour panels have a 21-day target ([East Genomics](https://www.eastgenomics.nhs.uk/about-us/quality/nhse-test-directory-turnaround-times/)), in Taiwan National Health Insurance reimburses next-generation sequencing once per lifetime and only at regional hospitals or above ([Health Promotion Administration](https://www.twhealth.org.tw/journalView.php?cat=70&sid=1190)).
![Sarcoma is not one disease: six subtypes, six genetic definitions, four treatment paths](business/fig_sarcoma_not_one_disease_biorender.jpg)

**Solution.** A model [(https://iressa-sarcoma-triage-demo.static.hf.space)](https://iressa-sarcoma-triage-demo.static.hf.space/) that reads the routine H&E slide already produced for every biopsy and returns, in minutes, a subtype probability and a recommendation for which genomic test to order first. It does not replace the test. It makes the first order the right one.
![AI in orthopaedics and MSK, 2018 to 2026: 15,504 PubMed records mapped onto the care pathway. Referral and triage is the thinnest stage](business/fig_ai_msk_pubmed_landscape.png)

**Efficiency lever.** One H&E slide plus one model call replaces up to three weeks of waiting and one avoidable round of testing per misrouted case.

![What the result looks like for the surgeon: one slide, one answer, one operation](business/fig_with_ai_happy_surgeon_biorender.png)

**Result so far.** A reproducible baseline on open TCGA-SARC data separates two common subtypes from slide overviews with an out-of-fold AUC of 0.82 on 60 patients, and runs live in the browser at <https://iressa-sarcoma-triage-demo.static.hf.space/>.

**What is in this submission.**

| File | Content |
|---|---|
| `technical/01_sarcoma_hne_triage.ipynb` | Working baseline on open TCGA-SARC data, 60 patients, out-of-fold AUC 0.82 |
| `technical/technical_report.md` | Section-by-section write-up of how the baseline model was built, trained and evaluated (Technical report, sections 1 to 10) |
| `technical/02_savings_model.ipynb` | Transparent savings arithmetic, every input labelled sourced or assumption |
| `technical/03_robustness_checks.ipynb` | Bootstrap interval, repeated splits, permutation null, calibration, stain perturbation, tile maps |
| `medicine/clinical_implementation.md` | Medical part: the clinical problem, where the AI sits, integration and safety, Taiwan, diversity, implementation stages |
| `business/business_case.md` | Business part on the NHS five-case model: strategic, economic, commercial, financial, management, including business model, competition, milestones, funding and patient involvement |
| `technical/requirements.txt`, `technical/fetch_overviews.py` | Environment and download helper |
| `group-member-contact/README.md` | Team and contributions |

