# Business case: H&E-first molecular triage for sarcoma

Prepared 1 October 2026 for the AI in Orthopaedics and MSK 2026 Hackathon. The baseline model is in `technical/01_sarcoma_hne_triage.ipynb`, the savings arithmetic in `technical/02_savings_model.ipynb`, the clinical pathway in `medicine/clinical_implementation.md`.

## 1. The problem we are solving

![Sarcoma is not one disease: six subtypes with six genetic definitions, one surgeon who has to choose between four different treatment pathways](business/fig_sarcoma_not_one_disease_biorender.jpg)

**Why the subtype matters.** A sarcoma is not one disease (Figure 7). More than 100 bone and soft tissue subtypes exist, and many are defined by a single pathognomonic gene fusion rather than by what the tumour looks like, for example Ewing sarcoma, synovial sarcoma and myxoid liposarcoma ([Sbaraglia 2021](https://doi.org/10.32074/1591-951X-213)). So the subtype is not a label added at the end. It is the first thing the surgical team has to know, because every later decision depends on it.

**What the subtype decides for the surgeon.** Three orthopaedic decisions follow directly from the subtype. First, whether to operate now or treat first: Ewing sarcoma and high-grade osteosarcoma receive several cycles of chemotherapy before any resection, whereas most adult soft tissue sarcomas go to surgery first ([ESMO bone sarcoma guideline, Strauss 2021](https://www.annalsofoncology.org/article/S0923-7534(21)04280-0/fulltext), [UK bone sarcoma guidelines 2024](https://www.nature.com/articles/s41416-024-02868-4)). Second, how wide to cut and whether the limb can be saved: the planned margin, the need for pre-operative radiotherapy, and the choice between limb-salvage reconstruction and amputation are all set by subtype and grade ([UK soft tissue sarcoma guidelines 2024](https://www.nature.com/articles/s41416-024-02674-y)). Third, who should operate and where: in England every suspected bone sarcoma must be referred to a designated centre such as the Royal National Orthopaedic Hospital, which with UCLH sees about 500 new sarcoma patients a year ([RNOH sarcoma unit](https://www.rnoh.nhs.uk/services/sarcoma-unit)). Operating on the wrong subtype means the wrong margin, the wrong sequence, or an avoidable amputation.

**Why the subtype is an efficiency problem.** The subtype is confirmed by a molecular test, and that test is slow and centralised. Figure 9 puts the three points side by side. Here is what it costs when the test is wrong or late, with the numbers.

- **England, the test.** Sarcoma genomic testing runs through seven Genomic Laboratory Hubs, with 54 sarcoma indications in the National Genomic Test Directory ([Birmingham Women's and Children's, genomic testing in sarcomas](https://bwc.nhs.uk/genomic-testing-in-sarcomas/)). The national standard for urgent solid tumour panels is 90 per cent reported within 21 days ([East Genomics, turnaround times](https://www.eastgenomics.nhs.uk/about-us/quality/nhse-test-directory-turnaround-times/)). The target is 90 per cent of tests reported within 21 days. In practice about one test in three is late: the only hub that publishes its figure delivers "over two thirds" on time and calls that "slightly above the national average" ([South East Genomics, turnaround times](https://southeastgenomics.nhs.uk/professionals/service-turn-around-times/)), and NHS England publishes no national figure at all ([Future Health, Keeping pace with cancer, 2024](https://www.futurehealth-research.com/publications/keeping-pace-with-cancer-accelerating-access-to-genomic-testing-through-the-nhs-genomic-medicine-service/)). So a request sent to the wrong panel is not a short delay. It is a second three-week wait at the back of a queue that is already running late.

- **England, the patient.** The delay is not only in the genetic test. The whole cancer pathway in England is already slower than its own target. In March 2026 only 72.8 per cent of patients began their first treatment within 62 days of an urgent referral; the target is 85 per cent ([NHS England Cancer Waiting Times, March 2026](https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2026/05/Cancer-Waiting-Times-Statistical-Release-March-2026-Provider-based-Provisional.pdf)). For sarcoma specifically, Sarcoma UK's National Sarcoma Survey found that 30 per cent of patients waited at least six months after first consulting a healthcare professional before an accurate diagnosis, 17 per cent waited more than a year, and 35 per cent saw a healthcare professional more than three times before being referred for tests ([Sarcoma UK, Delays cost lives, 2020](https://sarcoma.org.uk/wp-content/uploads/2022/05/early_diagnosis_rgb_single_pages_update_2.pdf)). The same report records that delay is associated with higher risk of metastasis and of amputation instead of limb-salvage surgery.
- **England, the surgery.** We know how often a sarcoma is operated on before anyone knows it is a sarcoma. According to PubMed, in 2,201 patients referred to the Royal Orthopaedic Hospital, Birmingham, 402 (18 per cent) had already undergone an unplanned excision elsewhere because the lump was not recognised as a sarcoma; 87 per cent needed a second operation, residual tumour was found in 59 per cent of them, and a positive margin in a high-grade tumour carried a 60 per cent risk of local recurrence even with radiotherapy ([Chandrasekar and colleagues, J Bone Joint Surg Br 2008](https://doi.org/10.1302/0301-620X.90B2.19760)). So nearly one patient in five has an operation that should not have happened, and more than half of them still have tumour left behind.

**The operation that should not happen, and how the model stops it.** This is the single most expensive failure in the pathway (Figure 8). A patient has a lump. The surgeon takes it for a benign lipoma and removes it whole. The pathology report then says sarcoma, with tumour at the cut edge. The patient needs a second, wider operation, often radiotherapy, and sometimes an amputation that a planned first operation would have avoided. With the model, the lump is biopsied first, the model reads the H&E and says "sarcoma, refer", and the first operation is done once, at a specialist centre, with the right margin. One condition must be stated plainly: the model can only help when a biopsy is taken before anything is removed. For a lump that is excised without a biopsy there is no slide to read. The proposal therefore pairs the model with the existing guideline rule, biopsy before excision for any suspicious lump, and measures how often that rule is followed as one of its outcomes.

![Today: a lump removed as benign turns out to be sarcoma and needs a second operation. With the model: biopsy first, the slide is read, the patient is referred, one correct operation|521x291](business/fig_unplanned_excision_biorender.jpg)

- **England, the money.** A 2025 cost study from a large English district general hospital put NHS hospital costs at about £11,200 per patient for an early-stage cancer diagnosis and about £23,800 for a late-stage diagnosis ([BMC Cost Effectiveness and Resource Allocation, 2025](https://link.springer.com/article/10.1186/s12962-025-00657-1)). Delayed and incorrect cancer diagnoses also cost NHS Resolution £81.5 million in damages and legal fees between April 2021 and March 2023 ([NHS Resolution review, summarised](https://www.boyesturner.com/insights/nhs-resolutions-review-cancer-diagnosis-delays)).
- **Taiwan, the rule.** Reimbursement is set by the National Health Insurance Administration under the National Health Insurance Act's fee schedule. From 1 May 2024 the NHIA pays for next-generation sequencing in 19 cancers at three fixed rates, NT$10,000 for BRCA, NT$20,000 for a small panel of up to 100 genes, NT$30,000 for a large panel, **once per person per cancer type for life**, with an estimated 20,000 patients a year and a budget of about NT$300 million ([NHIA press release, 2024](https://www.nhi.gov.tw/ch/cp-14565-e02e0-3255-1.html)). Only regional hospitals or above, or hospitals with cancer-care accreditation, listed under the Regulations Governing the Administration of Special Medical Technologies, Examinations, Devices and Equipment as approved laboratory-developed-test sites and running a molecular tumour board may claim it ([NHIA NGS payment Q&A, 2024](https://www.nhi.gov.tw/ch/dl-69957-04acdb972dc54e4ebb47fa3fab24b0fd-1.pdf)). District hospitals cannot order it in house.
- **Taiwan, the gap in evidence.** No published figure exists for how many Taiwanese sarcoma patients receive a misrouted first panel, how many referrals are wasted, or how many diagnoses are missed; the scheme is less than two years old and the NHIA has not released utilisation by cancer type. But the rule itself tells us the consequence. If the first panel is the wrong one, the patient's only reimbursed test is gone, and the second one is paid by the patient or not done at all. Producing those numbers is one of the first deliverables of the Taiwan validation arm.


![Why the subtype matters, what it decides for the surgeon, and why it is an efficiency problem](business/fig_subtype_three_points_biorender.jpg)

The bottleneck is not surgical capacity. It is three things that go wrong before the right operation. A lump is removed before anyone knows it is a sarcoma. A patient is referred to the specialist pathway who did not need it. And the surgical plan waits for weeks between the biopsy and the molecular answer. All three start at the same place, the first H&E slide at the referring hospital. The solution in the next section reads that slide on the day of the biopsy.

## 2. The solution

The model reads the routine H&E slide, inside the viewer the laboratory already uses, and returns within minutes two probabilities: is this a sarcoma, and which subtype.

the goal of it is to On day one it names the panel to order and how urgently, and flags slides that do not match the requested test.

 The orthopaedic oncologist therefore settles at the first meeting, not three weeks later, whether to give chemotherapy first, how wide the margin must be, and whether the limb can be saved.

![One H&E slide in, two probabilities out, and the three decisions the surgeon can then make](business/fig_model_outputs_biorender.jpg)

**What is in this submission.** Figure 10 shows the two outputs. The notebook here does a first step on the second only, two common subtypes on open TCGA data. The production model adds the first output and the fusion-defined subtypes.

**How it is built, and why the data meet the diversity and ethics criteria.** Training: open TCGA-SARC slides, then Royal National Orthopaedic Hospital slides under the biobank's existing ethics approval. Robustness: a UK dataset in which one tissue block was stained in 30 hospitals and scanned on 3 scanners. External validation: Taiwanese slides from the National Biobank Consortium, the first Asian cohort in any sarcoma AI. Results are reported by laboratory, scanner, sex, age and population. Patient data never crosses a border; only the model moves.

![The existing pathway in grey; the AI step inserted in blue; six weeks becomes three](business/fig_patient_pathway_model_fit_biorender.jpg)

**Where it sits.** Figure 11. Today the slide goes to the pathologist, a test is ordered, and a wrong panel repeats the loop; six weeks is common. With the model, one step is added between slide and pathologist. The pathologist reads the slide first, then the score. One correct test is ordered on day one; three weeks in total.

**How it plugs in.** No new hardware. The model runs as a module in the existing digital pathology viewer, as third-party AI already does through Sectra Amplifier ([example listing](https://amplifiermarketplace.sectra.com/vendor/panakeia/)). The result is written into the laboratory system next to the H&E report, with the model version for audit. The slide stays inside the hospital network. A working demo of the baseline, upload a slide and read the result, is live at <https://iressa-sarcoma-triage-demo.static.hf.space/> and in `demo/`.

![What the pathologist sees: (1) the slide, (2) the AI panel with model version, (3) sarcoma probability, (4) subtype probabilities, (5) the panel to order first and whether slide and request match, (6) the abstain threshold, (7) write to the laboratory system or disagree, (8) audit trail showing the slide never left the network and that the pathologist read first](business/fig_viewer_ui_mockup.png)

Figure 12 is a mock-up of that screen. The numbered parts are the only additions to the viewer the pathologist already uses.

**Aim.** The first genomic request is the right one for every sarcoma patient. Conservatively, about 2,900 patient-days of waiting removed a year in England and about 20 once-only reimbursed tests protected a year in Taiwan (`technical/02_savings_model.ipynb`). Payer and pricing are in sections 3, 8 and 13.

Efficiency lever: **one H&E slide plus one model call replaces up to three weeks of waiting and one avoidable round of testing per misrouted case.**

## 3. Who pays, and why they would

One payer in each country, two kinds of user, and one channel. Figure 13 shows the money and the use separately.

| Who | Role | What they buy | Why it is worth it to them |
|---|---|---|---|
| **NHS England, through the Genomic Laboratory Hubs** | Primary payer, England | Per-slide licence, or an annual regional subscription, delivered inside the hub's existing digital pathology feed | The hub pays for every genomic test from a central budget. Each misrouted request costs a repeat panel and a second three-week cycle against a 21-day national target. One licence replaces both. |
| **Taiwan National Health Insurance Administration** | Primary payer, Taiwan | A reimbursement code for AI-assisted pathology triage | NGS is paid once per patient per lifetime, capped at NT$30,000. A wrong first panel spends it. Triage protects it. |
| **Specialist sarcoma centres** (Royal National Orthopaedic Hospital, Birmingham, Oxford, Newcastle) | User, and the clinicians who ask the hub to buy | Nothing extra; the result arrives with the referral | The orthopaedic team has the subtype before the first multidisciplinary meeting, so the theatre booking, the margin and the limb-salvage decision are made three weeks earlier. |
| **District and regional hospitals** (both countries) | User | Nothing extra; the score appears in the viewer they already use | They cannot run genomic tests themselves. The score tells them whether to refer, and stops the lump being removed before anyone knows it is a sarcoma. |
| **Digital pathology marketplaces** (Sectra Amplifier, Leica) | Channel | A listed module, paid by revenue share | Scanner vendors do not buy rare-cancer models outright. They list them and take a share, which is how third-party pathology AI already reaches hospitals ([Sectra Amplifier listing](https://amplifiermarketplace.sectra.com/vendor/panakeia/)). |

**Price against cost.** Compute is under £0.10 a slide (section 13). One repeat genomic panel is about £339 ([2017 NHS figure](http://enseqlopedia.com/2017/03/cost-ngs-cancer-test-nhs-339/)). One unplanned excision followed by re-operation costs the system far more than that; management after an unplanned excision cost 64 per cent more than after a planned one in a Scandinavian series ([EJSO 2020](https://pubmed.ncbi.nlm.nih.gov/32037016/)). A per-slide fee in the tens of pounds therefore pays for itself on the first avoided repeat test, and many times over on the first avoided re-operation. The fee used in the financial projections is £40 a slide; it is an assumption until a hub quotes.

![Business model: who pays (green, money in), who uses (grey, result out), and the marketplace channel](business/fig_business_model_biorender.jpg)

## 4. Payment pathway


The figure (Figure 3) is in the summary section of the submission document and in `business/payment_pathway_biorender.jpg` ([editable BioRender version](https://app.biorender.com/illustrations/639f48d72cfd34c4f14311b2)). 

Flow: patient biopsy at a local hospital → H&E slide scanned → model call (charged per slide to the laboratory or hub) → triage report → correct genomic test ordered once → result reaches the sarcoma multidisciplinary team.

## 5. Adoption and roll-out


1. **Year 1, research use.** Validate on the Royal National Orthopaedic Hospital biobank and on the 30-hospital stain-variation dataset released by the UCL sarcoma group, which shows whether the model survives the change of laboratory and scanner ([Chai, Chen and colleagues, J Pathol Clin Res 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12932120/)).
2. **Year 2, shadow deployment** at one Genomic Laboratory Hub, model output recorded but not acted on, measuring how often it would have changed the ordered test.
3. **Year 3, regulated deployment** as a UKCA-marked decision support tool, and a parallel Taiwan pilot at one medical centre with NHI Administration as the reimbursement partner.

## 6. Diversity and ethics


Performance is reported separately by staining laboratory, scanner and population. The Taiwan arm exists because published sarcoma AI has been trained almost entirely on European and North American slides. Patient-level data are never moved. Only the model moves.

## 7. Scope of the prototype, and what the production model adds

The code in `technical/` is a proof of concept on open TCGA-SARC data, built so that any reviewer can rerun it on a laptop and get the same numbers. It shows that the H&E image alone separates two common sarcoma subtypes. The production model is a larger version of the same pipeline, not a different product. The table sets the two side by side; the Technical report, sections 1 to 8, gives the detail.

| | Prototype in this submission | Production model |
|---|---|---|
| Data | Open TCGA-SARC, 60 patients, LMS and DDLPS | Royal National Orthopaedic Hospital biobank, the UCL 30-hospital stain-variation set, Taiwan Biobank |
| Input | Slide overview, lowest resolution | Full-resolution tiles from the whole slide |
| Model | Frozen ImageNet ResNet50, tile features averaged | Pathology foundation model with attention pooling |
| Task | Two subtypes, out-of-fold AUC 0.82 | Sarcoma or not, then subtype including fusion-defined ones, with an abstain option |
| Runs as | Jupyter notebook and browser demo, CPU, seed 42 | Module inside the digital pathology viewer, output written to the laboratory system |

Moving from the prototype to the production model changes the data and the model. It does not change where the tool sits in the pathway or who acts on its output.

## 8. How much money it saves, and why a government payer pays


The arithmetic is in `technical/02_savings_model.ipynb`, with every input labelled SOURCED or ASSUMPTION so a reviewer can change any number and re-run.

| Input | Value | Status |
|---|---|---|
| New sarcoma cases, UK, per year | about 5,900 ([Sarcoma UK](https://sarcoma.org.uk/about-us/stay-connected/sarcoma-incidence-and-survival-statistics-in-the-uk/)) | sourced |
| Cost of one NHS NGS cancer panel | £339 ([2017 figure](http://enseqlopedia.com/2017/03/cost-ngs-cancer-test-nhs-339/), historic) | sourced, dated |
| Urgent solid tumour panel target | 90 per cent within 21 days ([East Genomics](https://www.eastgenomics.nhs.uk/about-us/quality/nhse-test-directory-turnaround-times/)) | sourced |
| Taiwan NHI NGS reimbursement | once per lifetime, cap NT$30,000 ([HPA summary](https://www.twhealth.org.tw/journalView.php?cat=70&sid=1190)) | sourced |
| Share of cases needing a molecular test | 0.50 | assumption |
| Share of those tests misrouted or repeated | 0.10 | assumption |
| Share of misroutes the triage catches | 0.70 | assumption |
| Days saved per caught misroute | 14 | assumption |

With those conservative assumptions the UK direct laboratory saving is about £70,000 a year and about 2,900 patient-days of waiting are removed. The direct saving is small because the test is cheap. The value is in the days, and in Taiwan in protecting a test that can only be reimbursed once.

Why the payer is the government and not the hospital:

1. In England cancer genomic tests are funded centrally by NHS England, so the avoided repeat and the triage licence sit on the same budget ([BWC genomics](https://bwc.nhs.uk/genomic-testing-in-adult-solid-tumours/)).
2. The 21-day target is a national performance measure for the Genomic Laboratory Hubs, so a tool that removes second cycles is bought to protect a target.
3. Taiwan NHI pays once per lifetime, so a wrong first order is an unrecoverable public cost.
4. Sarcoma is rare and referral is centralised, so one national licence covers the whole pathway.

The two assumptions a pilot must measure first are the misroute rate and the catch rate. The sensitivity plot in the notebook shows every input moves the result proportionally.

## 9. Ethics and regulation, the path we will follow


**What the tool is in law.** Software that triages patient data to influence a diagnostic decision is a medical device in the UK, UKCA-marked under the Medical Devices Regulations 2002, with a UK Approved Body audit for Class IIa and above ([MHRA view, clinician's guide](https://www.iatrox.com/blog/is-this-ai-tool-a-medical-device-uk-mhra-guide)). We plan for Class IIa, decision support that a pathologist confirms, never an autonomous result.

**Steps, in order.**

1. **Research phase, no device.** Retrospective work on open TCGA data and on biobank material under the biobank's existing ethics (RNOH Biobank, HTA licence 12055, REC 15/YH/0311, [RNOH biobank page](https://www.rnoh.nhs.uk/services/cellular-and-molecular-pathology/rnoh-biobank-and-research-programme)). No new patient contact, no new consent needed.
2. **Data protection.** A Data Protection Impact Assessment before any NHS slide leaves the laboratory network. Slides stay in the hub, the model is deployed to the data.
3. **NHS entry criteria.** Digital Technology Assessment Criteria, the NHS baseline covering clinical safety (DCB0129 and DCB0160), data protection, technical assurance, interoperability and accessibility ([NICE and DTAC overview](https://www.iatrox.com/blog/openevidence-chatgpt-5-medwise-ai-iatrox-uk-clinicians-dtac-nice-esf)).
4. **Evidence standard.** NICE Evidence Standards Framework for digital health technologies, tier C, which asks for comparative evidence of effectiveness and an economic impact case ([NICE ESF](https://www.nice.org.uk/corporate/ecd7/resources/evidence-standards-framework-for-digital-health-technologies-pdf-1124017457605)). Notebook 02 is the starting point for the economic case.
5. **Shadow deployment** at one Genomic Laboratory Hub, output recorded, not acted on, with a prospective protocol registered before the first case.
6. **UKCA technical file** and Approved Body audit, then a Taiwan TFDA submission in parallel using the same clinical evidence.

**Ethics commitments written into the design.**

- Performance reported by staining laboratory, scanner, sex, age group and ancestry, never as one pooled number. The 30-hospital dataset exists to make the laboratory split possible.
- A pathologist sees the H&E first and the model second, so automation bias is limited by workflow, not by a warning label.
- The model can abstain. Low-confidence cases are routed to the full panel, not to a guess.
- No patient-level data crosses a border. The Taiwan arm trains and validates inside Taiwan.
- Patient and public involvement before the shadow deployment, with the sarcoma patient charity as the first contact.

## 10. Business plan contents at a glance


| Section | Question it answers | Where |
|---|---|---|
| Problem and customer | Who hurts, how much, today | §1 |
| Solution and product | What it does, what it does not do | §2 |
| Market size | Number of cases, number of laboratories | §11 |
| Revenue model | Per-slide licence to hubs, national licence, OEM to scanner vendors | §3 |
| Competition | Who else does H&E-to-molecular prediction | §12 |
| Unit economics | Cost per inference against price per slide | §13 |
| Go-to-market | Year 1 research, year 2 shadow, year 3 regulated | §5 |
| Regulatory and ethics | Device class, evidence standard, data protection | §9 |
| Team | Clinician, ML lead, pathology partner, regulatory advisor | §14 |
| Risks | Model does not generalise, regulation slips, hubs do not adopt | §15 |
| Milestones and money | What each year costs and who funds it | §16 to §19 |
| Key performance indicators | Misroute rate, days to molecular result, abstention rate, per-site AUC | Listed in notebook 02 §5 and notebook 01 §9 |

## 11. Market size


| Market | Cases per year | Source |
|---|---|---|
| UK, all sarcoma | about 5,900 (700 bone, 5,200 soft tissue) | [Sarcoma UK statistics](https://sarcoma.org.uk/about-us/stay-connected/sarcoma-incidence-and-survival-statistics-in-the-uk/) |
| Taiwan, primary bone cancer | 1,238 cases in 2003 to 2010, about 155 a year, age-standardised rate 6.70 per million | [Hung and colleagues, Ann Surg Oncol 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4082651/) |
| Taiwan, soft tissue sarcoma | 3,843 cases in 2003 to 2011, about 430 a year, age-standardised rate 1.63 per 100,000 | [Medicine (Baltimore) 2015, Taiwan Cancer Registry](https://journals.lww.com/md-journal/fulltext/2015/10020/incidences_of_primary_soft_tissue_sarcoma.18.aspx) |

The Taiwan figures are a decade old and are used as a floor. The current annual report of the Taiwan Cancer Registry is the source to update from ([Health Promotion Administration registry reports](https://www.hpa.gov.tw/Pages/List.aspx?nodeid=119)). Laboratories: seven Genomic Laboratory Hubs in England ([BWC genomics](https://bwc.nhs.uk/genomic-testing-in-sarcomas/)); Taiwan NGS is restricted to regional hospitals and above ([HPA summary](https://www.twhealth.org.tw/journalView.php?cat=70&sid=1190)).

## 12. Competition


Nobody markets an H&E-to-fusion-gene product for sarcoma today. The category exists in other cancers, which proves the regulatory route and the buyer, and leaves sarcoma open.

| Company | Product | What it predicts from H&E | Regulatory status | Relevance |
|---|---|---|---|---|
| Owkin | MSIntuit CRC | Microsatellite instability in colorectal cancer, rules out about half of MSS patients at 96 per cent sensitivity | CE-marked ([EurekAlert, Nature Communications validation](https://www.eurekalert.org/news-releases/1007027)) | Closest business model, a pre-screen that reduces molecular tests |
| Panakeia | PANProfiler Breast | ER, PR, HER2 status | UKCA and CE ([Panakeia](https://www.panakeia.ai/post/ai-breast-cancer-diagnosis-technology-approved-for-uk-and-eu)) | UK company, same regulatory path we plan |
| Paige | Prostate Biomarker Suite, Paige Predict | AR amplification, TP53, RB1, PTEN in prostate; 123 biomarkers across 16 tumour types | CE-IVD and UKCA for prostate ([Business Wire 2022](https://www.businesswire.com/news/home/20220512005278/en/Paige-AI-Solution-for-Prostate-Cancer-Biomarker-Detection-Receives-CE-IVD-and-UKCA-Marks)); Predict launched under Tempus ([Stock Titan](https://www.stocktitan.net/news/TEM/tempus-announces-the-launch-of-paige-hh82yy4lw2gd.html)) | Largest player, no sarcoma model listed |
| Academic, UCL and RNOH | AI Scope sarcoma diagnosis, UKRI funded | Subtype from pathology plus genomics | Research ([UCL news 2023](https://www.ucl.ac.uk/engineering/news/2023/aug/sarcoma-research-benefits-part-ps13m-fund-ai-research-healthcare)) | Partner, not competitor |

Academic literature on sarcoma AI is prognosis-first, not fusion-first, for example survival prediction from H&E with reported AUC 0.97 in one cohort ([PMC review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11129162/)) and margin-aware prognosis in 2025 ([Scientific Reports 2025](https://www.nature.com/articles/s41598-025-20804-1)). A 2025 review frames fusion detection as the next AI target in soft tissue sarcoma genomics ([PubMed 41497157](https://pubmed.ncbi.nlm.nih.gov/41497157/)).

## 13. Unit economics


Per-slide inference cost, computed from public prices. Feature extraction with a pathology foundation model such as UNI takes about 2 to 5 minutes per whole slide on one GPU ([Scientific Reports 2025 retrieval study](https://www.nature.com/articles/s41598-025-88545-9), [ensemble study, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13564370)). An AWS g5.xlarge with one A10G costs about US$1.01 an hour on demand ([g5.xlarge pricing](https://calculator.holori.com/aws/ec2/g5.xlarge)).

| Item | Value | Basis |
|---|---|---|
| GPU time per slide | 5 minutes, upper bound | UNI extraction time above |
| GPU cost per slide | about US$0.08 | 5/60 × $1.01 |
| Storage per slide | 1 to 8 GB, about 2 GB compressed | [MDPI review of WSI](https://www.mdpi.com/2673-5261/7/1/2) |
| Storage cost | a 250,000-slide-a-year laboratory spends about US$90,000 a year | [Digital Pathology Association](https://digitalpathologyassociation.org/blog/dont-be-afraid-of-storage-costs) |
| Volume, UK | about 3,000 slides a year if half of new cases are triaged | §8 |

At that volume compute is under US$300 a year. The cost of the product is regulatory, clinical validation and support, not inference. A per-slide price in the tens of pounds is therefore almost pure margin once the device is certified, and a national licence should be priced against the days saved, not against compute.

## 14. Team, roles needed and who is in place


| Role | Needed for | Status |
|---|---|---|
| Clinical lead, orthopaedic and sarcoma | Problem definition, clinical implementation, MDT access | I-Han Cheng, MD, DPhil student NDORMS Oxford, team lead |
| Machine learning lead | Model, reproducibility, robustness testing | I-Han Cheng for this submission; production model needs a computational pathology partner |
| Pathology partner | Ground truth, slide access, stain-variation dataset | Planned partner: UCL sarcoma pathology group, contact opened 1 October 2026 |
| Genomics partner | Fusion labels, test-directory knowledge | Planned partner: a Genomic Laboratory Hub |
| Regulatory and health economics | UKCA file, NICE ESF economic case | Recruited at grant stage |
| Taiwan clinical partner | Asian validation cohort, NHI pilot | Planned partner: a Taiwan medical centre with NGS accreditation |

Contributions for this submission are recorded in `group-member-contact/README.md`.

## 15. Risks and mitigations


| Risk | Likelihood | Mitigation |
|---|---|---|
| Model learns stain colour, not biology, and fails at new sites | High, the published sarcoma foundation-model study shows accuracy falling from 0.94 to as low as 0.47 across institutions ([Chai and colleagues 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12932120/)) | Stain-variation dataset as a gate, stain normalisation, per-site reporting, abstention |
| Too few open slides for fusion subtypes | Certain today | Start with the two common subtypes, add RNOH and Taiwan biobank material under ethics |
| Regulatory timeline slips | Medium | Enter as Class IIa decision support, apply to the MHRA AI Airlock phase 3 from April 2026 ([GOV.UK AI Airlock](https://www.gov.uk/government/collections/ai-airlock-the-regulatory-sandbox-for-aiamd)) |
| Hubs do not adopt | Medium | Shadow deployment with a measured misroute rate before any purchase decision |
| Reimbursement not created in Taiwan | Medium | Pilot under NSTC smart-healthcare funding first, NHI code later |

## 16. Milestones and funding


| Year | Milestone | Funding route | Amount and source |
|---|---|---|---|
| 1, 2026 to 2027 | Production model on RNOH and TCGA slides, robustness on the 30-hospital set, first manuscript | NIHR i4i Product Development Award | No upper limit, typical £0.5 to £1.5 million ([NIHR i4i PDA](https://www.nihr.ac.uk/funding/i4i-product-development-awards-pda-nice-early-use-april-2026/2026400)); next round October 2026 ([RedKnight note](https://redknightconsultancy.co.uk/2026/09/09/nihr-i4i-product-development-awards-open-in-october-2026/)) |
| 1, parallel | Feasibility and business case | SBRI Healthcare phase 1 | Up to £100,000 for six months ([SBRI Healthcare cancer programme](https://sbrihealthcare.co.uk/competitions/sbri-healthcare-cancer-programme)) |
| 2, 2027 to 2028 | Shadow deployment at one hub, DTAC, NICE ESF evidence | Innovate UK Biomedical Catalyst | £25 million pool for industry-led small projects ([Innovate UK](https://grantedai.com/grants/biomedical-catalyst-industry-led-r-d-small-projects-innovate-uk-part-of-ukri-c8835f70)) |
| 2, parallel | Taiwan validation cohort | NSTC smart-healthcare innovation programme 2024 to 2027 ([NSTC](https://www.nstc.gov.tw/folksonomy/detail/fddf1cb6-469b-4c41-a9dc-dc93ba4170db?l=ch)) | Submission under the TFDA AI/ML software guidance ([TFDA guidance](https://www.fda.gov.tw/tc/includes/GetFile.ashx?id=f637354438894278725)) |
| 3, 2028 to 2029 | UKCA technical file, first paid licence | Licence revenue, SBRI phase 2 | |

## 17. Development timeline, how fast and what is delivered when


Three years from research prototype to first paid licence. Each quarter has one deliverable that can be checked.

| Quarter | Deliverable | Gate to pass |
|---|---|---|
| 2026 Q4 | Hackathon baseline on open data (this submission); **first grant application submitted, Cancer Research UK Early Detection and Diagnosis Primer Award** | AUC above chance on open data, done (0.82); primer application submitted |
| 2027 Q1 | Ethics amendment at the Royal National Orthopaedic Hospital biobank; TCGA full-resolution pipeline with a pathology foundation model | Access letter signed; feature extraction runs on 261 TCGA cases |
| 2027 Q2 | First fusion-subtype model (Ewing, synovial, myxoid liposarcoma) on RNOH plus TCGA | Per-subtype AUC reported with confidence intervals |
| 2027 Q3 | Robustness gate on the 30-hospital, 3-scanner dataset; stain normalisation on and off | Prediction drift across laboratories below a pre-registered threshold |
| 2027 Q4 | Manuscript submitted; Taiwan cohort request through the National Biobank Consortium; shadow-deployment protocol registered | Protocol on a public registry before first case |
| 2028 Q1 to Q2 | Shadow deployment at one Genomic Laboratory Hub; DTAC evidence collected | Misroute rate measured with and without the model |
| 2028 Q3 to Q4 | Taiwan external validation; NICE Evidence Standards Framework economic case; UKCA technical file drafted | Per-population performance reported |
| 2029 Q1 to Q2 | Approved Body audit; MHRA registration; TFDA submission | Certificate issued |
| 2029 Q3 onward | First paid licence to a hub; advisory-mode deployment | Contract signed |

## 18. How much money, line by line


Three-year budget. Sourced lines carry a link; the rest are labelled assumptions and should be replaced by quotes before any grant is submitted.

| Line | Year 1 | Year 2 | Year 3 | Basis |
|---|---|---|---|---|
| Machine learning researcher, 1.0 FTE | £60,000 | £62,000 | £64,000 | Oxford research grade 7, £39,424 to £47,779 salary ([Oxford salary scales](https://www.ox.ac.uk/about/jobs/working-here/pay-and-reward/salary-scales)), plus about 30 per cent on-costs, assumption |
| Clinical lead time, 0.2 FTE | £15,000 | £15,000 | £15,000 | Assumption, buy-out of clinical sessions |
| Pathology annotation and slide scanning | £20,000 | £10,000 | £5,000 | Assumption, scanning and pathologist time at RNOH |
| GPU compute | £2,000 | £3,000 | £3,000 | About US$0.08 per slide at g5.xlarge rates ([AWS g5.xlarge](https://calculator.holori.com/aws/ec2/g5.xlarge)); mostly training, not inference |
| Taiwan cohort, specimen processing fees | £0 | £15,000 | £5,000 | National Biobank Consortium publishes a fee schedule ([NBCT application area](https://nbct.nhri.org.tw/mainList.aspx?uid=19&pid=19)); amount is an assumption until quoted |
| Regulatory consultancy and Approved Body audit | £0 | £20,000 | £40,000 | Third-party UKCA assessment is charged at £200 to £500 an hour and totals from the low thousands upward for a Class IIa software device ([UKCA guide](https://euverify.com/resource/ukca-testing-and-certification/)); MHRA registration about £300 a year per device category from April 2026 ([Casus Consulting](https://casusconsulting.com/uk-mhra-to-implement-annual-medical-device-registration-fees-starting-april-2026/)); clinical safety officer time is the larger part, assumption |
| Health economics and NICE ESF evidence | £0 | £15,000 | £10,000 | Assumption, contracted |
| Patient and public involvement | £3,000 | £3,000 | £2,000 | Assumption, sarcoma charity partnership |
| Travel, dissemination, open-access fees | £5,000 | £7,000 | £7,000 | Assumption |
| **Total** | **£105,000** | **£150,000** | **£151,000** | **About £406,000 over three years** |

The number to defend is the regulatory line. Everything else is ordinary research cost. If the Approved Body quote comes back higher, the roll-out shifts by a quarter, not the model.

## 19. Where the money comes from, and who is actively giving


Ranked by fit, with the next deadline where it is published.

| Funder and scheme | Amount | Fit | Deadline or status | Source |
|---|---|---|---|---|
| **Sarcoma UK, Open Grant Round 2026** | Pilot up to £75,000, Project up to £200,000 | High, sarcoma-specific, diagnosis is a named priority | Round closed 10 September 2026, next round 2027 | [Sarcoma UK open grant round](https://sarcoma.org.uk/our-research/apply-for-research-funding/open-grant-round-2025/) |
| **Sarcoma UK, Improving Sarcoma Diagnosis fund** | Per call | Highest, the call names this problem | Rolling, see the Sarcoma UK site | [Improving sarcoma diagnosis](https://sarcoma.org.uk/our-research/apply-for-research-funding/improving-sarcoma-diagnosis-funding-round/) |
| **Sarcoma UK, Early Career Sarcoma Research Fund** | Per call | High, DPhil students eligible | Rolling, see the Sarcoma UK site | [Early career fund](https://sarcoma.org.uk/our-research/apply-for-research-funding/early-career-sarcoma-research-fund/) |
| **Bone Cancer Research Trust, Idea Grant and Ewing sarcoma project call** | Project call up to £250,000 | High for the Ewing arm, a fusion-defined subtype | 2026 calls closed 31 July and 1 June; annual | [BCRT for researchers](https://www.bcrt.org.uk/research/for-researchers/) |
| **Cancer Research UK, Early Detection and Diagnosis Primer Award** | Up to £100,000, one year | High, pays for exactly the year-1 feasibility work | Rolling rounds | [CRUK primer award](https://www.cancerresearchuk.org/for-researchers/apply-for-and-manage-your-funding/our-funding-schemes/early-detection-diagnosis-primer-award) |
| **NIHR i4i Product Development Award** | No upper limit, typically £0.5 to £1.5 million | High for years 2 to 3, covers regulatory and clinical evaluation | Round opens October 2026 | [NIHR i4i PDA](https://www.nihr.ac.uk/funding/i4i-product-development-awards-pda-nice-early-use-april-2026/2026400) |
| **SBRI Healthcare, NHS Cancer Programme** | Phase 1 up to £100,000 for six months | Medium to high, NHS-facing feasibility | Open calls announced on the site | [SBRI Healthcare cancer programme](https://sbrihealthcare.co.uk/competitions/sbri-healthcare-cancer-programme) |
| **Innovate UK Biomedical Catalyst** | £25 million pool, industry-led small projects | Medium, needs an SME or spin-out partner | Annual | [Innovate UK](https://grantedai.com/grants/biomedical-catalyst-industry-led-r-d-small-projects-innovate-uk-part-of-ukri-c8835f70) |
| **EMERGE RehabTech Pacesetter** (seen at ICNR 2026) | Phase 3 awards up to £30,000 for market analysis, grants 1 January to 30 June 2027 | Low to medium, rehabilitation technology focus, but the training and mentoring phases are open to UK clinicians and the business-plan coaching is directly useful | Round 1 closed 19 June 2026, Phase 1 workshop 14 July 2026, next round not yet announced; contact EMERGErehabtech@ntu.ac.uk | [Medilink Midlands](https://www.medilinkmidlands.com/applications-now-open-emerge-rehabtech-pacesetter/), [EMERGE](https://emergerehabtech.org/) |
| **Taiwan NSTC smart-healthcare innovation programme 2024 to 2027** | Varies; bilateral AI calls about NT$5 million a year per project | High for the Taiwan validation arm | Calls listed on the NSTC site | [NSTC](https://www.nstc.gov.tw/folksonomy/detail/fddf1cb6-469b-4c41-a9dc-dc93ba4170db?l=ch) |
| **MHRA AI Airlock, phase 3** | Not a grant, a regulatory sandbox | High for de-risking the device route | From April 2026, three years | [GOV.UK AI Airlock](https://www.gov.uk/government/collections/ai-airlock-the-regulatory-sandbox-for-aiamd) |

**Funding plan in one line.** We will start by applying for the Cancer Research UK Early Detection and Diagnosis Primer Award, up to £100,000 for one year, because it is the fastest route to a first grant, it carries the lowest entry barrier for an early-career applicant, and it covers the year-1 budget almost exactly. Sarcoma UK's pilot grant (£75,000) is the parallel application in the next round, and SBRI phase 1 tops up year 1. Years 2 and 3 are covered by one NIHR i4i award. Taiwan is covered by NSTC. The three-year total of about £406,000 fits inside that stack with margin.

**Who is actively giving right now.** Sarcoma UK and the Bone Cancer Research Trust run annual sarcoma-specific calls and have named diagnosis as a priority. Cancer Research UK's primer award is the fastest route to a first £100,000. The EMERGE Pacesetter seen at ICNR is a business-plan accelerator rather than a research funder, and it is rehabilitation-focused, so it is a place to learn the pitch, not the place to fund the model.

