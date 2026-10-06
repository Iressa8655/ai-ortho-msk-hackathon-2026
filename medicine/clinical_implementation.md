# Clinical background and implementation strategy

Prepared 1 October 2026 for the AI in Orthopaedics and MSK 2026 Hackathon. The model is in `technical/01_sarcoma_hne_triage.ipynb`, the payer case in `business/business_case.md`.

## 1. The clinical problem


Sarcomas are rare cancers of bone and soft tissue, about 5,900 new UK cases a year ([Sarcoma UK](https://sarcoma.org.uk/about-us/stay-connected/sarcoma-incidence-and-survival-statistics-in-the-uk/)). More than 100 subtypes exist and the subtype decides the operation, the margin, and whether chemotherapy is given. Many subtypes are defined by a single genetic event, a gene fusion, rather than by appearance alone ([WHO classification overview](https://doi.org/10.32074/1591-951X-213)).

The diagnostic pathway today:

1. A lump is imaged and biopsied at a local hospital.
2. The H&E slide is read by a general pathologist, who suspects sarcoma.
3. The case is referred to one of the designated sarcoma centres. All suspected bone sarcomas in England must go to such a centre ([RNOH sarcoma unit](https://www.rnoh.nhs.uk/services/sarcoma-unit)).
4. The specialist pathologist orders immunohistochemistry and a genomic test through the Genomic Laboratory Hub. The national target for urgent solid tumour panels is 90 per cent reported within 21 days ([East Genomics](https://www.eastgenomics.nhs.uk/about-us/quality/nhse-test-directory-turnaround-times/)).
5. The multidisciplinary team meets when the molecular result is back.

Where the time goes: steps 3 and 4. A misrouted or repeated genomic request adds a full cycle.

## 2. Where the AI sits


Between step 2 and step 3. The H&E slide that already exists is scanned and scored. The output is a probability for each subtype and a recommendation for which genomic test to order first. The pathologist sees the slide before the score. The score never replaces the genomic test and never generates a report on its own.

Efficiency lever: the right genomic test is ordered on day one at the referring hospital, so the sarcoma centre receives a case with the molecular result already in progress.

## 3. Implementation, step by step


| Stage | What happens | Who owns it | Measure of success |
|---|---|---|---|
| Retrospective validation | Model run on archived cases with known fusion status at one sarcoma centre and on the 30-hospital stain-variation dataset | Research team with the centre's pathology department | Per-subtype AUC, per-laboratory AUC, abstention rate |
| Shadow mode | Model scores live cases, output recorded, not shown to clinicians | One Genomic Laboratory Hub | Misroute rate with and without the model, measured on the same cases |
| Advisory mode | Score shown to the specialist pathologist as a second opinion at the point of test ordering | Sarcoma centre pathology | Days from biopsy to molecular result, repeat-test rate |
| Referral triage | Score available to the referring general pathologist | Regional pathology network | Proportion of referrals arriving with the correct test already ordered |

## 4. Integration


The model runs inside the laboratory's existing digital pathology system. Slides do not leave the network. Output is a structured field in the laboratory information system alongside the H&E report, with the model version and confidence recorded for audit. Vendors already provide marketplace integration for third-party AI, for example Sectra Amplifier ([Panakeia on Sectra](https://amplifiermarketplace.sectra.com/vendor/panakeia/)), so no new viewer is needed.

## 5. Safety design


- The pathologist reads the H&E first. The score appears after the first read, to limit automation bias.
- Low-confidence cases are labelled "no recommendation" and follow the current pathway unchanged.
- Every score is logged with the model version, the scanner and the staining laboratory, so drift at a single site is visible within weeks.
- The model is retrained only under a documented change-control plan, matching the regulator's expectations for adaptive AI ([TFDA predetermined change control guidance](https://www.fda.gov.tw/TC/siteListContent.aspx?sid=11652&id=47477); the MHRA takes the same approach through the AI Airlock, [GOV.UK](https://www.gov.uk/government/collections/ai-airlock-the-regulatory-sandbox-for-aiamd)).

## 6. Taiwan


The same tool at a Taiwan medical centre. National Health Insurance reimburses next-generation sequencing once per lifetime, capped at NT$30,000, and only regional hospitals and above may perform it ([Health Promotion Administration](https://www.twhealth.org.tw/journalView.php?cat=70&sid=1190)). District hospitals therefore refer without a molecular result. An H&E triage score tells them whether and where to refer, and protects the single reimbursed test from being spent on the wrong panel.

## 7. Diversity and equity


Sarcoma AI has been trained almost entirely on European and North American slides. Performance is reported separately by laboratory, scanner, sex, age group and ancestry, and the Taiwan cohort exists so that an Asian population is in the validation set from the start, not as an afterthought.

