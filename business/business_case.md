# Business part: business case and business plan

Structured on the five-case model that NHS and HM Treasury business cases use ([HM Treasury Green Book, five-case model](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)): strategic, economic, commercial, financial, management. Sections are numbered in reading order; the map in section 1 shows the five parts on one page.

## Part A. Strategic case: the problem, the solution, and why now

The case for change. Sarcoma subtype decides the operation and the oncology plan, the confirming genomic test is centralised and slow, and a wrong first order costs a full test cycle in England and the single reimbursed test in Taiwan. We propose decision support that reads the H&E slide already in hand and makes the first genomic order the right one. This part states the problem, the solution, and what the submitted prototype does and does not prove.

### 1. Map of this business case

The five parts follow the five-case model used for NHS and HM Treasury business cases ([Green Book](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government)). Each part answers one question, and the sections under it are read in order (Figure 19).

![The five parts and the sections under each](business/fig_five_case_map.png)

| Part | Question it answers | Sections |
| ------------- | ------------------------------------------------------------------------------------------------------------------- | -------- |
| A. Strategic | What is wrong today and what we propose; the clinical evidence is in the Medical part | 1 to 3 |
| B. Economic | What the payer saves and what one slide costs to run | 4, 5 |
| C. Commercial | Who pays, how the money flows, how big the market is, who else sells | 6 to 9 |
| D. Financial | What three years cost and who funds them | 10 to 12 |
| E. Management | How it is rolled out, by when, under which regulation, with patients involved how, by whom, and what could go wrong | 13 to 18 |

Key performance indicators: misroute rate, days to molecular result, abstention rate and per-site AUC, listed in notebook 02 section 5 and notebook 01 section 9.

### 2. The problem we are solving: three target problems

![Three target problems on the diagnostic pathway, all starting at the first H&E slide](business/fig_three_target_problems.png)

Figure 20 marks the three failures on the pathway. The bottleneck is not surgical capacity. It is three things that go wrong before the right operation. (1) A lump is removed before anyone knows it is a sarcoma. (2) A patient is referred to the specialist pathway who did not need it. (3) The surgical plan waits for weeks between the biopsy and the molecular answer. All three start at the same place, the first H&E slide at the referring hospital. The clinical evidence, the pathway and the costs of each failure are set out in the Medical part, section 1.

### 3. The solution, as a product

A decision-support module inside the digital pathology viewer the laboratory already uses. It reads the routine H&E slide and returns two probabilities, is this a sarcoma and which subtype, with the genomic panel to order first. Where it sits in the pathway, what the pathologist sees, and how it is integrated and kept safe are in the Medical part, sections 2 and 3.

**How it is built, and why the data meet the diversity and ethics criteria.** Training: open TCGA-SARC slides, then Royal National Orthopaedic Hospital slides under the biobank's existing ethics approval. Robustness: a UK dataset in which one tissue block was stained in 30 hospitals and scanned on 3 scanners. External validation: Taiwanese slides from the National Biobank Consortium, the first Asian cohort in any sarcoma AI. NBCT confirmed on 2 October 2026 that bone sarcoma tissue with images and pathology reports is available to a Taiwan-based co-investigator (Medical part, section 4); it is not public data, so it is not used in this submission. Results are reported by laboratory, scanner, sex, age and population. Patient data never crosses a border; only the model moves.

**Aim.** The first genomic request is the right one for every sarcoma patient. Conservatively, about 2,900 patient-days of waiting removed a year in England and about 20 once-only reimbursed tests protected a year in Taiwan (`technical/02_savings_model.ipynb`). Payer and pricing are in sections 4, 5 and 6.

Efficiency lever: **one H&E slide plus one model call replaces up to three weeks of waiting and one avoidable round of testing per misrouted case.**

## Part B. Economic case: what it saves and what it costs to run

Value for money. The direct laboratory saving is modest because the test is cheap; the value is in patient-days of waiting removed and operations planned with the subtype known. Inference cost per slide is negligible, so the cost of the service is validation, regulation and support. Every input is labelled sourced or assumption and can be changed in the savings notebook.

### 4. How much money it saves, and why a government payer pays


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

### 5. Unit economics


Per-slide inference cost, computed from public prices. Feature extraction with a pathology foundation model such as UNI takes about 2 to 5 minutes per whole slide on one GPU ([Scientific Reports 2025 retrieval study](https://www.nature.com/articles/s41598-025-88545-9), [ensemble study, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13564370)). An AWS g5.xlarge with one A10G costs about US$1.01 an hour on demand ([g5.xlarge pricing](https://calculator.holori.com/aws/ec2/g5.xlarge)).

| Item | Value | Basis |
|---|---|---|
| GPU time per slide | 5 minutes, upper bound | UNI extraction time above |
| GPU cost per slide | about US$0.08 | 5/60 × $1.01 |
| Storage per slide | 1 to 8 GB, about 2 GB compressed | [MDPI review of WSI](https://www.mdpi.com/2673-5261/7/1/2) |
| Storage cost | a 250,000-slide-a-year laboratory spends about US$90,000 a year | [Digital Pathology Association](https://digitalpathologyassociation.org/blog/dont-be-afraid-of-storage-costs) |
| Volume, UK | about 3,000 slides a year if half of new cases are triaged | §4 |

At that volume compute is under US$300 a year. The cost of the product is regulatory, clinical validation and support, not inference. A per-slide price in the tens of pounds is therefore almost pure margin once the device is certified, and a national licence should be priced against the days saved, not against compute.

## Part C. Commercial case: who buys, how they pay, and who else sells

The buyer and the deal. One payer in each country, NHS England through the Genomic Laboratory Hubs and the National Health Insurance Administration in Taiwan, and two kinds of user who pay nothing extra. The product reaches them inside the digital pathology viewer they already use. No company sells an H&E-to-fusion product for sarcoma today.

### 6. Who pays, and why they would

One payer in each country, two kinds of user, and one channel. Figure 21 shows the money and the use separately.

| Who | Role | What they buy | Why it is worth it to them |
|---|---|---|---|
| **NHS England, through the Genomic Laboratory Hubs** | Primary payer, England | Per-slide licence, or an annual regional subscription, delivered inside the hub's existing digital pathology feed | The hub pays for every genomic test from a central budget. Each misrouted request costs a repeat panel and a second three-week cycle against a 21-day national target. One licence replaces both. |
| **Taiwan National Health Insurance Administration** | Primary payer, Taiwan | A reimbursement code for AI-assisted pathology triage | NGS is paid once per patient per lifetime, capped at NT$30,000. A wrong first panel spends it. Triage protects it. |
| **Specialist sarcoma centres** (Royal National Orthopaedic Hospital, Birmingham, Oxford where the team lead is based, Newcastle) | User, and the clinicians who ask the hub to buy | Nothing extra; the result arrives with the referral | The orthopaedic team has the subtype before the first multidisciplinary meeting, so the theatre booking, the margin and the limb-salvage decision are made three weeks earlier. |
| **District and regional hospitals** (both countries) | User | Nothing extra; the score appears in the viewer they already use | They cannot run genomic tests themselves. The score tells them whether to refer, and stops the lump being removed before anyone knows it is a sarcoma. |
| **Digital pathology marketplaces** (Sectra Amplifier, Leica) | Channel | A listed module, paid by revenue share | Scanner vendors do not buy rare-cancer models outright. They list them and take a share, which is how third-party pathology AI already reaches hospitals ([Sectra Amplifier listing](https://amplifiermarketplace.sectra.com/vendor/panakeia/)). |

**Price against cost.** Compute is under £0.10 a slide (section 6). One repeat genomic panel is about £339 ([2017 NHS figure](http://enseqlopedia.com/2017/03/cost-ngs-cancer-test-nhs-339/)). One unplanned excision followed by re-operation costs the system far more than that; management after an unplanned excision cost 64 per cent more than after a planned one in a Scandinavian series ([EJSO 2020](https://pubmed.ncbi.nlm.nih.gov/32037016/)). A per-slide fee in the tens of pounds therefore pays for itself on the first avoided repeat test, and many times over on the first avoided re-operation. The fee used in the financial projections is £40 a slide; it is an assumption until a hub quotes.

![Business model: who pays (green, money in), who uses (grey, result out), and the marketplace channel](business/fig_business_model_biorender.jpg)

### 7. Payment pathway


Figure 22 shows who pays whom along the diagnostic pathway. Grey arrows carry the sample and the report, green arrows carry money. The source file is `business/payment_pathway_biorender.jpg` ([editable BioRender version](https://app.biorender.com/illustrations/639f48d72cfd34c4f14311b2)). 

Flow: patient biopsy at a local hospital → H&E slide scanned → model call (charged per slide to the laboratory or hub) → triage report → correct genomic test ordered once → result reaches the sarcoma multidisciplinary team.

![Payment pathway: sample and report in grey, money in green](business/payment_pathway_biorender.jpg)

### 8. Market size


| Market | Cases per year | Source |
|---|---|---|
| UK, all sarcoma | about 5,900 (700 bone, 5,200 soft tissue) | [Sarcoma UK statistics](https://sarcoma.org.uk/about-us/stay-connected/sarcoma-incidence-and-survival-statistics-in-the-uk/) |
| Taiwan, primary bone cancer | 1,238 cases in 2003 to 2010, about 155 a year, age-standardised rate 6.70 per million | [Hung and colleagues, Ann Surg Oncol 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4082651/) |
| Taiwan, soft tissue sarcoma | 3,843 cases in 2003 to 2011, about 430 a year, age-standardised rate 1.63 per 100,000 | [Medicine (Baltimore) 2015, Taiwan Cancer Registry](https://journals.lww.com/md-journal/fulltext/2015/10020/incidences_of_primary_soft_tissue_sarcoma.18.aspx) |

The Taiwan figures are a decade old and are used as a floor. The current annual report of the Taiwan Cancer Registry is the source to update from ([Health Promotion Administration registry reports](https://www.hpa.gov.tw/Pages/List.aspx?nodeid=119)). Laboratories: seven Genomic Laboratory Hubs in England ([BWC genomics](https://bwc.nhs.uk/genomic-testing-in-sarcomas/)); Taiwan NGS is restricted to regional hospitals and above ([HPA summary](https://www.twhealth.org.tw/journalView.php?cat=70&sid=1190)).

### 9. Competition


Nobody markets an H&E-to-fusion-gene product for sarcoma today. The category exists in other cancers, which proves the regulatory route and the buyer, and leaves sarcoma open.

| Company | Product | What it predicts from H&E | Regulatory status | Relevance |
|---|---|---|---|---|
| Owkin | MSIntuit CRC | Microsatellite instability in colorectal cancer, rules out about half of MSS patients at 96 per cent sensitivity | CE-marked ([EurekAlert, Nature Communications validation](https://www.eurekalert.org/news-releases/1007027)) | Closest business model, a pre-screen that reduces molecular tests |
| Panakeia | PANProfiler Breast | ER, PR, HER2 status | UKCA and CE ([Panakeia](https://www.panakeia.ai/post/ai-breast-cancer-diagnosis-technology-approved-for-uk-and-eu)) | UK company, same regulatory path we plan |
| Paige | Prostate Biomarker Suite, Paige Predict | AR amplification, TP53, RB1, PTEN in prostate; 123 biomarkers across 16 tumour types | CE-IVD and UKCA for prostate ([Business Wire 2022](https://www.businesswire.com/news/home/20220512005278/en/Paige-AI-Solution-for-Prostate-Cancer-Biomarker-Detection-Receives-CE-IVD-and-UKCA-Marks)); Predict launched under Tempus ([Stock Titan](https://www.stocktitan.net/news/TEM/tempus-announces-the-launch-of-paige-hh82yy4lw2gd.html)) | Largest player, no sarcoma model listed |
| Academic, UCL and RNOH | AI Scope sarcoma diagnosis, UKRI funded | Subtype from pathology plus genomics | Research ([UCL news 2023](https://www.ucl.ac.uk/engineering/news/2023/aug/sarcoma-research-benefits-part-ps13m-fund-ai-research-healthcare)) | Partner, not competitor |

Academic literature on sarcoma AI is prognosis-first, not fusion-first, for example survival prediction from H&E with reported AUC 0.97 in one cohort ([PMC review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11129162/)) and margin-aware prognosis in 2025 ([Scientific Reports 2025](https://www.nature.com/articles/s41598-025-20804-1)). A 2025 review frames fusion detection as the next AI target in soft tissue sarcoma genomics ([PubMed 41497157](https://pubmed.ncbi.nlm.nih.gov/41497157/)).

**Where the effort is, counted.** Figure 23 puts numbers on the two claims above, from PubMed counts run in `technical/04_competitor_landscape.ipynb` on 7 October 2026 with the queries printed in that notebook. Sarcoma AI publishing grew from 20 records in 2018 to 270 in 2025 but stayed at about 1.1 to 1.5 per cent of all cancer AI records (panel A). Within sarcoma AI, prognosis (537 records) and histology diagnosis (400) lead; molecular or biomarker prediction from H&E is at most 251 on a broad keyword match, and few of those predict a fusion gene (panel B). Deep-learning H&E-to-molecular work is an order of magnitude larger in breast (1,692), lung (1,620) and colorectal cancer (1,098) than in sarcoma (182) (panel C), and the regulated products follow the same pattern: colorectal, breast and prostate have one each, sarcoma has none (panel D). Keyword counts overlap and overcount; the figure is a map of effort, not a systematic review.

![Where the competition is, and where it is not: PubMed counts by year, task and tumour type, and the regulated products by tumour type](business/fig_competitor_landscape.png)

## Part D. Financial case: budget and funders

Affordability. Three years from prototype to first licence, grant-funded so that the first contract is signed with evidence rather than a price guess. The budget is itemised line by line and each line is marked sourced or assumption. The first application is the Cancer Research UK Early Detection and Diagnosis Primer Award.

### 10. Milestones and funding


| Year | Milestone | Funding route | Amount and source |
|---|---|---|---|
| 1, 2026 to 2027 | Production model on RNOH and TCGA slides, robustness on the 30-hospital set, first manuscript | NIHR i4i Product Development Award | No upper limit, typical £0.5 to £1.5 million ([NIHR i4i PDA](https://www.nihr.ac.uk/funding/i4i-product-development-awards-pda-nice-early-use-april-2026/2026400)); next round October 2026 ([RedKnight note](https://redknightconsultancy.co.uk/2026/09/09/nihr-i4i-product-development-awards-open-in-october-2026/)) |
| 1, parallel | Feasibility and business case | SBRI Healthcare phase 1 | Up to £100,000 for six months ([SBRI Healthcare cancer programme](https://sbrihealthcare.co.uk/competitions/sbri-healthcare-cancer-programme)) |
| 2, 2027 to 2028 | Shadow deployment at one hub, DTAC, NICE ESF evidence | Innovate UK Biomedical Catalyst | £25 million pool for industry-led small projects ([Innovate UK](https://grantedai.com/grants/biomedical-catalyst-industry-led-r-d-small-projects-innovate-uk-part-of-ukri-c8835f70)) |
| 2, parallel | Taiwan validation cohort | NSTC smart-healthcare innovation programme 2024 to 2027 ([NSTC](https://www.nstc.gov.tw/folksonomy/detail/fddf1cb6-469b-4c41-a9dc-dc93ba4170db?l=ch)) | Submission under the TFDA AI/ML software guidance ([TFDA guidance](https://www.fda.gov.tw/tc/includes/GetFile.ashx?id=f637354438894278725)) |
| 3, 2028 to 2029 | UKCA technical file, first paid licence | Licence revenue, SBRI phase 2 | |

### 11. How much money, line by line


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

### 12. Where the money comes from, and who is actively giving


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

## Part E. Management case: delivery, regulation, team and risks

Deliverability. Research use, then shadow deployment at one hub, then regulated use as UKCA-marked Class IIa decision support that a pathologist confirms. Performance is reported by laboratory, scanner and population, and the single largest risk, a model that learns stain colour instead of biology, has a measured gate before any clinical use.

### 13. Adoption and roll-out


1. **Year 1, research use.** Validate on the Royal National Orthopaedic Hospital biobank and on the 30-hospital stain-variation dataset released by the UCL sarcoma group, which shows whether the model survives the change of laboratory and scanner ([Chai, Chen and colleagues, J Pathol Clin Res 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12932120/)).
2. **Year 2, shadow deployment** at one Genomic Laboratory Hub, model output recorded but not acted on, measuring how often it would have changed the ordered test.
3. **Year 3, regulated deployment** as a UKCA-marked decision support tool, and a parallel Taiwan pilot at one medical centre with NHI Administration as the reimbursement partner.

The clinical stages inside each year, with who owns each and how success is measured, are in the Medical part, section 6.

### 14. Development timeline, how fast and what is delivered when


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

### 15. Ethics and regulation, the path we will follow


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

### 16. Patient and public involvement

Patients are involved from the first year, not after the device exists.

1. **A patient advisory panel in year 1**, formed with Sarcoma UK and the Bone Cancer Research Trust, both of which fund and support patient involvement in sarcoma research ([Sarcoma UK, Improving Sarcoma Diagnosis](https://sarcoma.org.uk/our-research/apply-for-research-funding/improving-sarcoma-diagnosis-funding-round/), [BCRT for researchers](https://www.bcrt.org.uk/research/for-researchers/)). The panel co-writes the patient-facing explanation of what the tool does and does not do: it does not diagnose, it makes the first genomic order the right one.
2. **What patients feel during the wait is measured, not assumed.** During the year 2 shadow deployment the panel helps design a short patient-reported experience measure on the wait between biopsy and molecular result, so that the days saved in section 4 can be paired with what those days mean to a patient.
3. **The panel reads the fairness reporting.** Performance by sex, age, laboratory, scanner and population (Medical part, section 5) is written up in a plain public summary that the panel approves before it is published.
4. **The panel sits on the advisory board** named in section 17, so the patient voice is in the room when the roll-out decisions in section 13 are made.

This is the patient and public involvement that the NHS Digital Technology Assessment Criteria and the NICE Evidence Standards Framework expect for a tool of this class ([NICE ESF](https://www.nice.org.uk/corporate/ecd7/resources/evidence-standards-framework-for-digital-health-technologies-pdf-1124017457605)). The partnerships with the two charities are planned, not yet agreed.

### 17. Team, roles needed and who is in place


| Role | Needed for | Status |
| -------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Clinical lead, orthopaedic and sarcoma | Problem definition, clinical implementation, MDT access | I-Han Cheng, MD, DPhil student NDORMS Oxford, team lead |
| Machine learning lead | Model, reproducibility, robustness testing | I-Han Cheng for this submission; production model needs a computational pathology partner |
| Clinical and tissue partner, Oxford | Sarcoma cases, HTA-approved tissue, multidisciplinary team access | Future partner, in house: the team lead is based at NDORMS in the Botnar Research Centre. The Oxford Sarcoma Service at the Nuffield Orthopaedic Centre is one of five national bone sarcoma centres, about 400 new patients a year, with a prospective HTA-approved tissue collection ([Oxford Sarcoma Service](https://www.ouh.nhs.uk/oxfordsarcomaservice/information/clinicians/)); the Oxford Musculoskeletal Biobank at Botnar is the department's sample resource ([OMB](https://directory.biobankinguk.org/Profile/Biobank/GBR-1-181)). Contact to be opened through the DPhil supervisors |
| Pathology partner | Ground truth, slide access, stain-variation dataset | Planned partner: UCL sarcoma pathology group, contact opened 1 October 2026 |
| Genomics partner | Fusion labels, test-directory knowledge | Planned partner: a Genomic Laboratory Hub |
| Regulatory and health economics | UKCA file, NICE ESF economic case | Recruited at grant stage |
| Taiwan clinical partner | Asian validation cohort, NHI pilot | Planned partner: a Taiwan medical centre with NGS accreditation |

Contributions for this submission are recorded in `group-member-contact/README.md`.

I-Han Cheng, team lead and sole member. Problem definition, data selection, model design, both notebooks, clinical implementation strategy, business case. Partners approached for the production phase, not authors of this submission: UCL sarcoma pathology group.

The clinical implementation strategy and the business case follow on the next pages.

### 18. Risks and mitigations


| Risk | Likelihood | Mitigation |
|---|---|---|
| Model learns stain colour, not biology, and fails at new sites | High, the published sarcoma foundation-model study shows accuracy falling from 0.94 to as low as 0.47 across institutions ([Chai and colleagues 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12932120/)) | Stain-variation dataset as a gate, stain normalisation, per-site reporting, abstention |
| Too few open slides for fusion subtypes | Certain today | Start with the two common subtypes, add RNOH and Taiwan biobank material under ethics |
| Regulatory timeline slips | Medium | Enter as Class IIa decision support, apply to the MHRA AI Airlock phase 3 from April 2026 ([GOV.UK AI Airlock](https://www.gov.uk/government/collections/ai-airlock-the-regulatory-sandbox-for-aiamd)) |
| Hubs do not adopt | Medium | Shadow deployment with a measured misroute rate before any purchase decision |
| Reimbursement not created in Taiwan | Medium | Pilot under NSTC smart-healthcare funding first, NHI code later |

