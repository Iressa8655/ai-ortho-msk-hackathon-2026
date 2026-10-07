# Business plan in the SBA traditional format

Nine sections, following the U.S. Small Business Administration's traditional business plan outline ([SBA, Write your business plan](https://www.sba.gov/business-guide/plan-your-business/write-your-business-plan)). Each section opens with the SBA's own one-line instruction, then the answer for this project. Numbers are sourced where a link is given; every unsourced number is labelled an assumption. Figures and arithmetic are in `technical/02_savings_model.ipynb` and `business/business_case.md`.

## 1. Executive summary


*SBA: "Briefly tell your reader what your company is and why it will be successful. Include your mission statement, your product or service, and basic information about your company's leadership team, employees, and location."*

**Mission.** Make the first genomic test the right one for every sarcoma patient, by reading the H&E slide that already exists.

**Product.** Decision-support software that scores a routine H&E whole-slide image in minutes and returns a probability for each fusion-defined sarcoma subtype together with a recommendation for which genomic panel to order first. It is used by the pathologist, never alone.

**Why it will succeed.** The category already exists and is reimbursed in other cancers: Owkin's MSIntuit for colorectal cancer is CE-marked ([EurekAlert](https://www.eurekalert.org/news-releases/1007027)), Panakeia's breast biomarker tool is UKCA-marked ([Panakeia](https://www.panakeia.ai/post/ai-breast-cancer-diagnosis-technology-approved-for-uk-and-eu)), Paige's prostate suite is CE-IVD and UKCA ([Business Wire](https://www.businesswire.com/news/home/20220512005278/en/Paige-AI-Solution-for-Prostate-Cancer-Biomarker-Detection-Receives-CE-IVD-and-UKCA-Marks)). Nobody has built it for sarcoma, where the subtype is molecular by definition and the test is centralised and slow.

**Leadership and location.** I-Han Cheng, MD, DPhil student at the Nuffield Department of Orthopaedics, Rheumatology and Musculoskeletal Sciences, University of Oxford. One founder at present. Planned partners: the UCL and Royal National Orthopaedic Hospital sarcoma pathology group, one NHS Genomic Laboratory Hub, one Taiwan medical centre. Location: Oxford, with a Taiwan validation arm.

**Proof so far.** A reproducible baseline on open TCGA-SARC data separates two common subtypes from slide overviews with an out-of-fold AUC of 0.82 on 60 patients (`technical/01_sarcoma_hne_triage.ipynb`).

## 2. Company description

*SBA: "Use your company description to provide detailed information about your company. Go into detail about the problems your business solves."*

**The problem and who we serve.** Set out in the business case, section 1 (the problem) and section 3 (who pays and who uses it). In one line: the sarcoma subtype decides the operation, the confirming genomic test is slow and centralised, and a wrong first order costs a full cycle in England and the single reimbursed test in Taiwan.

**Competitive advantage.** Three things nobody else holds together: clinical access to the largest UK sarcoma service through the planned UCL and Royal National Orthopaedic Hospital partnership, the only public 30-hospital, 3-scanner stain-variation dataset for sarcoma as a robustness gate ([Chai and colleagues 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12932120/)), and an Asian validation cohort through Taiwan's National Biobank Consortium, which no published sarcoma AI has.

**Legal structure.** Not yet incorporated. The research phase runs inside the University of Oxford. The planned route is a university spin-out through Oxford University Innovation at the point of the first NIHR i4i award, with intellectual property assigned under the university's standard terms. This is an assumption to confirm with Oxford University Innovation.

## 3. Market analysis

*SBA: "You'll need a good understanding of your industry outlook and target market. Competitive research will show you what other businesses are doing and what their strengths are."*

**Industry outlook.** Digital pathology is moving from scanning to AI-assisted reporting, with marketplace integration already in clinical use, for example Sectra Amplifier hosting third-party AI ([Panakeia on Sectra](https://amplifiermarketplace.sectra.com/vendor/panakeia/)). H&E-to-molecular prediction is the fastest-growing product class in that market because it sells a test result without a new test.

**Target market and competitors.** The case counts by country, the number of laboratories, and the competitor table are in the business case, sections 11 and 12. The short version: about 5,900 UK sarcoma cases a year, seven Genomic Laboratory Hubs, and no company listing a sarcoma product. Owkin, Panakeia and Paige have proven the regulatory route and the buyer in other cancers. Their strength is scale and marketplace presence. Our answer is a rare-disease niche they have not entered, with clinical partners they do not have.

## 4. Organisation and management

*SBA: "Tell your reader how your company will be structured and who will run it. Describe the legal structure of your business."*

**Who.** The roles, who fills them today and which are recruited at grant stage are in the business case, section 14.

**Structure.** A research project inside the University of Oxford until the first product-development award, then a spin-out limited company with the university and the founder as shareholders. An advisory board of a sarcoma pathologist, a genomic laboratory director and a patient representative is planned before shadow deployment.

## 5. Service or product line

*SBA: "Describe what you sell or what service you offer. Explain how it benefits your customers and what the product lifecycle looks like."*

**What we sell.** A per-slide inference service, deployed inside the laboratory's digital pathology system, returning a structured triage report: subtype probabilities, a recommended first genomic panel, a confidence flag, and an abstain option.

**Benefit.** The right test ordered once, on day one, at the referring hospital. In England that removes the second 21-day cycle for misrouted cases. In Taiwan it protects the single reimbursed test.

**Lifecycle.** Research prototype on open data (this submission), production model, robustness-gated version, shadow deployment, then UKCA-marked Class IIa decision support. The quarter-by-quarter plan is in the business case, section 17, and the regulatory steps in section 9.

**Intellectual property.** Model weights, the stain-robust training recipe and the triage reporting format. Foundation models are used under their published licences. This is a dependency to check before commercial use.

## 6. Marketing and sales

*SBA: "Your goal in this section is to describe how you'll attract and retain customers. You'll also describe how a sale will actually happen."*

**Who buys.** NHS England through the Genomic Laboratory Hubs, and the National Health Insurance Administration in Taiwan. Why each of them would pay is in the business case, section 3.

**How a sale happens.** Shadow deployment at one Genomic Laboratory Hub produces a measured misroute rate with and without the model. That number, with the economic case in the NICE Evidence Standards Framework format ([NICE ESF](https://www.nice.org.uk/corporate/ecd7/resources/evidence-standards-framework-for-digital-health-technologies-pdf-1124017457605)), is the sales document. The first contract is a site licence with that hub, the second is a national licence negotiated with NHS England specialised commissioning.

**Channels.** Direct to hubs and sarcoma centres; marketplace listing on the scanner vendors' platforms (Sectra, Leica, Hamamatsu, 3DHistech) as an OEM module; the sarcoma charity and the British Sarcoma Group meetings for clinical awareness.

**Retention.** Per-site performance dashboards, drift alerts by laboratory and scanner, and an annual revalidation report delivered as part of the licence.

## 7. Funding request

*SBA: "If you're asking for funding, this is where you'll outline your funding requirements. Your goal is to clearly explain how much funding you'll need."*

**Amount.** About £406,000 over three years. The line-by-line budget is in the business case, section 18, and the funders, with deadlines, in section 19.

**Type.** Grant funding, not equity, for the full three years. The regulatory line (£60,000) is the one to defend. The rest is ordinary research cost.

**Use of funds.** Salaries and clinical time 63 per cent, regulatory and health economics 21 per cent, data and compute 9 per cent, dissemination and patient involvement 7 per cent.

## 8. Financial projections

*SBA: "Supplement your funding request with financial projections. Your goal is to convince the reader that your business is stable and will be a success."*

All revenue figures below are assumptions, because no price has been agreed with any buyer. They are shown so the break-even logic can be checked and replaced. The cost side (compute and storage per slide) is in the business case, section 13, and the savings to the payer in section 8.

| Item | Value | Status |
|---|---|---|
| Price per slide to a hub | £40 | assumption |
| UK slides triaged a year at full adoption | about 3,000 | assumption, half of new cases |
| UK revenue a year at full adoption | about £120,000 | derived |
| National licence alternative | priced against patient-days saved, about 2,900 a year in the conservative model | derived, `02_savings_model.ipynb` |
| Taiwan revenue a year, 300 slides at NT$1,500 | about NT$450,000, about £11,000 | assumption |

**Break-even.** With fixed costs of about £150,000 a year in years 2 and 3 and a contribution of about £40 per slide, break-even on per-slide pricing needs about 3,750 slides a year, more than the whole UK sarcoma volume. The business therefore does not break even on UK per-slide fees alone. It breaks even on one of three routes: a national licence priced on days saved instead of slides, an OEM module sold through scanner vendors across several countries, or extension to the next fusion-defined tumour types (paediatric and gastrointestinal stromal tumours) that reuse the same pipeline. The three-year plan is grant-funded precisely so that the first licence is signed with evidence in hand, not with a price guess.

**Cash-flow shape.** Grants in, no revenue, years 1 to 2. First licence revenue year 3 Q3. The projection assumes the i4i award is secured. If it is not, year 2 compresses to the shadow deployment alone and the regulatory file slips a year.

## 9. Appendix

*SBA: an optional section for supporting documents.*

The supporting files are listed in the submission summary, section 1, and the technical report documents the notebook section by section.

