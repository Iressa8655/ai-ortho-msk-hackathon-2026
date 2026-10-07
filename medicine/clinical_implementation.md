# Medical part: clinical implementation strategy

The clinical problem, where the AI sits in the pathway, how it is integrated and kept safe, the Taiwan setting, diversity and equity, and the stages of clinical implementation.

## 1. The clinical problem

![Sarcoma is not one disease: six subtypes with six genetic definitions, one surgeon who has to choose between four different treatment pathways](business/fig_sarcoma_not_one_disease_biorender.jpg)

**Why the subtype matters.** A sarcoma is not one disease (Figure 6). More than 100 bone and soft tissue subtypes exist, and many are defined by a single pathognomonic gene fusion rather than by what the tumour looks like, for example Ewing sarcoma, synovial sarcoma and myxoid liposarcoma ([Sbaraglia 2021](https://doi.org/10.32074/1591-951X-213)). So the subtype is not a label added at the end. It is the first thing the surgical team has to know, because every later decision depends on it.

**What the subtype decides for the surgeon.** Three orthopaedic decisions follow directly from the subtype. First, whether to operate now or treat first: Ewing sarcoma and high-grade osteosarcoma receive several cycles of chemotherapy before any resection, whereas most adult soft tissue sarcomas go to surgery first ([ESMO bone sarcoma guideline, Strauss 2021](https://www.annalsofoncology.org/article/S0923-7534(21)04280-0/fulltext), [UK bone sarcoma guidelines 2024](https://www.nature.com/articles/s41416-024-02868-4)). Second, how wide to cut and whether the limb can be saved: the planned margin, the need for pre-operative radiotherapy, and the choice between limb-salvage reconstruction and amputation are all set by subtype and grade ([UK soft tissue sarcoma guidelines 2024](https://www.nature.com/articles/s41416-024-02674-y)). Third, who should operate and where: in England every suspected bone sarcoma must be referred to a designated centre such as the Royal National Orthopaedic Hospital, which with UCLH sees about 500 new sarcoma patients a year ([RNOH sarcoma unit](https://www.rnoh.nhs.uk/services/sarcoma-unit)). Operating on the wrong subtype means the wrong margin, the wrong sequence, or an avoidable amputation.

The diagnostic pathway today:

1. A lump is imaged and biopsied at a local hospital.
2. The H&E slide is read by a general pathologist, who suspects sarcoma.
3. The case is referred to one of the designated sarcoma centres. All suspected bone sarcomas in England must go to such a centre ([RNOH sarcoma unit](https://www.rnoh.nhs.uk/services/sarcoma-unit)).
4. The specialist pathologist orders immunohistochemistry and a genomic test through the Genomic Laboratory Hub. The national target for urgent solid tumour panels is 90 per cent reported within 21 days ([East Genomics](https://www.eastgenomics.nhs.uk/about-us/quality/nhse-test-directory-turnaround-times/)).
5. The multidisciplinary team meets when the molecular result is back.

Where the time goes: steps 3 and 4. A misrouted or repeated genomic request adds a full cycle.

**Why the subtype is an efficiency problem.** The subtype is confirmed by a molecular test, and that test is slow and centralised. Figure 8 puts the three points side by side. Here is what it costs when the test is wrong or late, with the numbers.

- **England, the test.** Sarcoma genomic testing runs through seven Genomic Laboratory Hubs, with 54 sarcoma indications in the National Genomic Test Directory ([Birmingham Women's and Children's, genomic testing in sarcomas](https://bwc.nhs.uk/genomic-testing-in-sarcomas/)). The national standard for urgent solid tumour panels is 90 per cent reported within 21 days ([East Genomics, turnaround times](https://www.eastgenomics.nhs.uk/about-us/quality/nhse-test-directory-turnaround-times/)). The target is 90 per cent of tests reported within 21 days. In practice about one test in three is late: the only hub that publishes its figure delivers "over two thirds" on time and calls that "slightly above the national average" ([South East Genomics, turnaround times](https://southeastgenomics.nhs.uk/professionals/service-turn-around-times/)), and NHS England publishes no national figure at all ([Future Health, Keeping pace with cancer, 2024](https://www.futurehealth-research.com/publications/keeping-pace-with-cancer-accelerating-access-to-genomic-testing-through-the-nhs-genomic-medicine-service/)). So a request sent to the wrong panel is not a short delay. It is a second three-week wait at the back of a queue that is already running late.

- **England, the patient.** The delay is not only in the genetic test. The whole cancer pathway in England is already slower than its own target. In March 2026 only 72.8 per cent of patients began their first treatment within 62 days of an urgent referral; the target is 85 per cent ([NHS England Cancer Waiting Times, March 2026](https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2026/05/Cancer-Waiting-Times-Statistical-Release-March-2026-Provider-based-Provisional.pdf)). For sarcoma specifically, Sarcoma UK's National Sarcoma Survey found that 30 per cent of patients waited at least six months after first consulting a healthcare professional before an accurate diagnosis, 17 per cent waited more than a year, and 35 per cent saw a healthcare professional more than three times before being referred for tests ([Sarcoma UK, Delays cost lives, 2020](https://sarcoma.org.uk/wp-content/uploads/2022/05/early_diagnosis_rgb_single_pages_update_2.pdf)). The same report records that delay is associated with higher risk of metastasis and of amputation instead of limb-salvage surgery.
- **England, the surgery.** We know how often a sarcoma is operated on before anyone knows it is a sarcoma. According to PubMed, in 2,201 patients referred to the Royal Orthopaedic Hospital, Birmingham, 402 (18 per cent) had already undergone an unplanned excision elsewhere because the lump was not recognised as a sarcoma; 87 per cent needed a second operation, residual tumour was found in 59 per cent of them, and a positive margin in a high-grade tumour carried a 60 per cent risk of local recurrence even with radiotherapy ([Chandrasekar and colleagues, J Bone Joint Surg Br 2008](https://doi.org/10.1302/0301-620X.90B2.19760)). So nearly one patient in five has an operation that should not have happened, and more than half of them still have tumour left behind.

**The operation that should not happen, and how the model stops it.** This is the single most expensive failure in the pathway (Figure 7). A patient has a lump. The surgeon takes it for a benign lipoma and removes it whole. The pathology report then says sarcoma, with tumour at the cut edge. The patient needs a second, wider operation, often radiotherapy, and sometimes an amputation that a planned first operation would have avoided. With the model, the lump is biopsied first, the model reads the H&E and says "sarcoma, refer", and the first operation is done once, at a specialist centre, with the right margin. One condition must be stated plainly: the model can only help when a biopsy is taken before anything is removed. For a lump that is excised without a biopsy there is no slide to read. The proposal therefore pairs the model with the existing guideline rule, biopsy before excision for any suspicious lump, and measures how often that rule is followed as one of its outcomes.

![Today: a lump removed as benign turns out to be sarcoma and needs a second operation. With the model: biopsy first, the slide is read, the patient is referred, one correct operation|521x291](business/fig_unplanned_excision_biorender.jpg)

- **England, the money.** A 2025 cost study from a large English district general hospital put NHS hospital costs at about £11,200 per patient for an early-stage cancer diagnosis and about £23,800 for a late-stage diagnosis ([BMC Cost Effectiveness and Resource Allocation, 2025](https://link.springer.com/article/10.1186/s12962-025-00657-1)). Delayed and incorrect cancer diagnoses also cost NHS Resolution £81.5 million in damages and legal fees between April 2021 and March 2023 ([NHS Resolution review, summarised](https://www.boyesturner.com/insights/nhs-resolutions-review-cancer-diagnosis-delays)).
- **Taiwan, the rule.** Reimbursement is set by the National Health Insurance Administration under the National Health Insurance Act's fee schedule. From 1 May 2024 the NHIA pays for next-generation sequencing in 19 cancers at three fixed rates, NT$10,000 for BRCA, NT$20,000 for a small panel of up to 100 genes, NT$30,000 for a large panel, **once per person per cancer type for life**, with an estimated 20,000 patients a year and a budget of about NT$300 million ([NHIA press release, 2024](https://www.nhi.gov.tw/ch/cp-14565-e02e0-3255-1.html)). Only regional hospitals or above, or hospitals with cancer-care accreditation, listed under the Regulations Governing the Administration of Special Medical Technologies, Examinations, Devices and Equipment as approved laboratory-developed-test sites and running a molecular tumour board may claim it ([NHIA NGS payment Q&A, 2024](https://www.nhi.gov.tw/ch/dl-69957-04acdb972dc54e4ebb47fa3fab24b0fd-1.pdf)). District hospitals cannot order it in house.
- **Taiwan, the gap in evidence.** No published figure exists for how many Taiwanese sarcoma patients receive a misrouted first panel, how many referrals are wasted, or how many diagnoses are missed; the scheme is less than two years old and the NHIA has not released utilisation by cancer type. But the rule itself tells us the consequence. If the first panel is the wrong one, the patient's only reimbursed test is gone, and the second one is paid by the patient or not done at all. Producing those numbers is one of the first deliverables of the Taiwan validation arm.


![Why the subtype matters, what it decides for the surgeon, and why it is an efficiency problem](business/fig_subtype_three_points_biorender.jpg)

The bottleneck is not surgical capacity. It is three things that go wrong before the right operation. A lump is removed before anyone knows it is a sarcoma. A patient is referred to the specialist pathway who did not need it. And the surgical plan waits for weeks between the biopsy and the molecular answer. All three start at the same place, the first H&E slide at the referring hospital. The next section shows where a model that reads that slide on the day of the biopsy sits in this pathway.

## 2. Where the AI sits, and what it returns

Between step 2 and step 3. The H&E slide that already exists is scanned and scored. The output is a probability for each subtype and a recommendation for which genomic test to order first. The pathologist sees the slide before the score. The score never replaces the genomic test and never generates a report on its own.

The model reads the routine H&E slide, inside the viewer the laboratory already uses, and returns within minutes two probabilities: is this a sarcoma, and which subtype.

the goal of it is to On day one it names the panel to order and how urgently, and flags slides that do not match the requested test.

 The orthopaedic oncologist therefore settles at the first meeting, not three weeks later, whether to give chemotherapy first, how wide the margin must be, and whether the limb can be saved.

![One H&E slide in, two probabilities out, and the three decisions the surgeon can then make](business/fig_model_outputs_biorender.jpg)

**What is in this submission.** Figure 9 shows the two outputs. The notebook here does a first step on the second only, two common subtypes on open TCGA data. The production model adds the first output and the fusion-defined subtypes.

![The existing pathway in grey; the AI step inserted in blue; six weeks becomes three](business/fig_patient_pathway_model_fit_biorender.jpg)

**Where it sits.** Figure 10. Today the slide goes to the pathologist, a test is ordered, and a wrong panel repeats the loop; six weeks is common. With the model, one step is added between slide and pathologist. The pathologist reads the slide first, then the score. One correct test is ordered on day one; three weeks in total.

Efficiency lever: the right genomic test is ordered on day one at the referring hospital, so the sarcoma centre receives a case with the molecular result already in progress.

## 3. Integration and safety

**How it plugs in.** No new hardware. The model runs as a module in the existing digital pathology viewer, as third-party AI already does through Sectra Amplifier ([example listing](https://amplifiermarketplace.sectra.com/vendor/panakeia/)). The result is written into the laboratory system next to the H&E report, with the model version for audit. The slide stays inside the hospital network. A working demo of the baseline, upload a slide and read the result, is live at <https://iressa-sarcoma-triage-demo.static.hf.space/> and in `demo/`.

The model runs inside the laboratory's existing digital pathology system. Slides do not leave the network. Output is a structured field in the laboratory information system alongside the H&E report, with the model version and confidence recorded for audit. Vendors already provide marketplace integration for third-party AI, for example Sectra Amplifier ([Panakeia on Sectra](https://amplifiermarketplace.sectra.com/vendor/panakeia/)), so no new viewer is needed.

![What the pathologist sees: (1) the slide, (2) the AI panel with model version, (3) sarcoma probability, (4) subtype probabilities, (5) the panel to order first and whether slide and request match, (6) the abstain threshold, (7) write to the laboratory system or disagree, (8) audit trail showing the slide never left the network and that the pathologist read first](business/fig_viewer_ui_mockup.png)

Figure 11 is a mock-up of that screen. The numbered parts are the only additions to the viewer the pathologist already uses.

**Safety design.**

- The pathologist reads the H&E first. The score appears after the first read, to limit automation bias.
- Low-confidence cases are labelled "no recommendation" and follow the current pathway unchanged.
- Every score is logged with the model version, the scanner and the staining laboratory, so drift at a single site is visible within weeks.
- The model is retrained only under a documented change-control plan, matching the regulator's expectations for adaptive AI ([TFDA predetermined change control guidance](https://www.fda.gov.tw/TC/siteListContent.aspx?sid=11652&id=47477); the MHRA takes the same approach through the AI Airlock, [GOV.UK](https://www.gov.uk/government/collections/ai-airlock-the-regulatory-sandbox-for-aiamd)).

## 4. Taiwan


The same tool at a Taiwan medical centre. National Health Insurance reimburses next-generation sequencing once per lifetime, capped at NT$30,000, and only regional hospitals and above may perform it ([Health Promotion Administration](https://www.twhealth.org.tw/journalView.php?cat=70&sid=1190)). District hospitals therefore refer without a molecular result. An H&E triage score tells them whether and where to refer, and protects the single reimbursed test from being spent on the wrong panel.

## 5. Diversity and equity


Sarcoma AI has been trained almost entirely on European and North American slides. Performance is reported separately by laboratory, scanner, sex, age group and ancestry, and the Taiwan cohort exists so that an Asian population is in the validation set from the start, not as an afterthought.

Patient-level data are never moved between countries or institutions. Only the model moves.

## 6. Clinical implementation, stage by stage


| Stage | What happens | Who owns it | Measure of success |
|---|---|---|---|
| Retrospective validation | Model run on archived cases with known fusion status at one sarcoma centre and on the 30-hospital stain-variation dataset | Research team with the centre's pathology department | Per-subtype AUC, per-laboratory AUC, abstention rate |
| Shadow mode | Model scores live cases, output recorded, not shown to clinicians | One Genomic Laboratory Hub | Misroute rate with and without the model, measured on the same cases |
| Advisory mode | Score shown to the specialist pathologist as a second opinion at the point of test ordering | Sarcoma centre pathology | Days from biopsy to molecular result, repeat-test rate |
| Referral triage | Score available to the referring general pathologist | Regional pathology network | Proportion of referrals arriving with the correct test already ordered |

