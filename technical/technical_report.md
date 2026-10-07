# Technical report, how the baseline model was built

This file is assembled from the vault review pages T01 to T08. It documents the notebook `01_sarcoma_hne_triage.ipynb` section by section: data, tiling, features, training, errors, the browser demo, and the gap to the production model.

## 1. Pipeline at a glance

Everything in this section is in one notebook, `technical/01_sarcoma_hne_triage.ipynb`, which runs end to end on a laptop CPU in about an hour, most of it download time. Figure 4 shows the six steps. Each step is one notebook section, with the story above the code, a comment on every line, and the output explained below it.

![The six steps of the baseline, one notebook section each](technical/figures/fig0_pipeline.png)

The design choice behind every step is the same: the smallest thing that proves the overview image carries subtype signal, so that a reviewer can rerun it and get the same number. Nothing is trained from scratch, nothing needs a GPU, and the random seed is fixed at 42.

## 2. Data, open TCGA-SARC slides

**Source.** The Cancer Genome Atlas sarcoma project (TCGA-SARC) holds diagnostic whole-slide images that are open access through the Genomic Data Commons API ([GDC TCGA-SARC](https://portal.gdc.cancer.gov/projects/TCGA-SARC)). Notebook section 2 lists every diagnostic slide with its file size, patient and primary diagnosis.

| Listed | Count |
|---|---|
| Diagnostic slides | 600 |
| Patients | 254 |
| Leiomyosarcoma (LMS) slides | 142 |
| Dedifferentiated liposarcoma (DDLPS) slides | 71 |

**Why these two subtypes.** They are the two largest well-defined groups in TCGA-SARC, and they lead to different first tests in practice: DDLPS is confirmed by MDM2 amplification, LMS by smooth-muscle immunohistochemistry. The fusion-defined subtypes that are the clinical goal of the project (Ewing, synovial, myxoid liposarcoma) have too few open slides to train on today.

**Cohort.** One slide per patient, so no patient can appear in both the training and the test fold. Thirty patients per class. We took the thirty smallest files per class because the lowest pyramid level scales with file size and reads faster. This is a selection bias and it is stated as such in section 8.

**What is read.** Only the lowest pyramid level of each slide, fetched over HTTP range requests with `fetch_overviews.py`, about 30 seconds per slide. The whole dataset is sixty small PNG files instead of sixty gigabytes, which is why anyone can rerun the notebook. Figure 5 shows two overviews per class.

![Slide overviews, lowest pyramid level, two per class](technical/figures/fig1_example_overviews.png)

## 3. Tiling and tissue mask

ResNet50 expects 224 px squares, so notebook section 5 slides a 224 px window with no overlap across each overview. A tile is kept only if at least 40 per cent of its pixels are darker than near-white (grey value below 220), which removes glass and most pen marks. Slides with fewer than three tissue tiles would be dropped; none were.

| Class | Slides | Mean tiles | Min | Max |
|---|---|---|---|---|
| DDLPS | 30 | 70.5 | 3 | 129 |
| LMS | 30 | 48.1 | 6 | 105 |

DDLPS slides give more tiles because the tumours are larger and fattier. The count itself cannot leak into the classifier, because the next step averages all tiles into one vector per slide (Figure 6).

![Tissue tiles per slide by class](technical/figures/fig2_tiles_per_slide.png)

## 4. Features, frozen ResNet50

Notebook section 6 passes every tile through a ResNet50 with ImageNet weights (torchvision `IMAGENET1K_V2`), with the classification head removed, so each tile becomes a 2048-dimensional vector. The vectors of one slide are averaged, giving a 60 by 2048 matrix, one row per patient. The CNN is not trained or fine-tuned at any point.

This is the cheapest credible baseline. It runs on a CPU in minutes and has no hyperparameters to tune, so the result cannot be an artefact of tuning on sixty patients. The production model replaces this step with a pathology foundation model on full-resolution tiles (section 8).

## 5. Training and cross-validation

Sixty patients cannot support anything bigger than a linear model. Notebook section 7 fits a standard scaler and a logistic regression (C = 0.1, L2 penalty) inside a 5-fold stratified cross-validation, seed 42. Stratification keeps the class ratio in every fold, and one slide per patient means no patient is in both train and test. Every number reported is out-of-fold: the model that scored a patient never saw that patient.

| Fold | AUC |
|---|---|
| 0 | 0.778 |
| 1 | 0.722 |
| 2 | 1.000 |
| 3 | 0.917 |
| 4 | 0.611 |
| **Out-of-fold, all 60** | **0.822** |

At a 0.5 threshold 42 of 60 patients are correct, nine errors in each class (Figure 1). The spread between folds, 0.61 to 1.00, is what twelve-patient test folds look like. It is a limit of the cohort size, not a bug.

![ROC curve and confusion matrix, out-of-fold](technical/figures/fig3_roc_confusion.png)

## 6. Where it fails

Notebook section 8 ranks the patients by how confidently wrong the model was. All four worst cases are DDLPS slides scored as LMS with p(DDLPS) below 0.08 (Figure 2).

| Case | True | File size (MB) | Tiles | p(DDLPS) |
|---|---|---|---|---|
| TCGA-WK-A8XQ | DDLPS | 1043 | 48 | 0.02 |
| TCGA-3R-A8YX | DDLPS | 440 | 31 | 0.05 |
| TCGA-DX-A2IZ | DDLPS | 1789 | 86 | 0.05 |
| TCGA-IF-A3RQ | DDLPS | 889 | 46 | 0.07 |

The overviews show why. Large well-differentiated fatty regions or necrotic areas dominate the slide, and a plain mean over tiles cannot separate a small high-grade component from the rest. These four slides define the next iteration: full-resolution tiles so nuclear detail is visible, and attention pooling so the model can weight the informative tiles instead of averaging them away.

![Most confident errors, all DDLPS scored as LMS](technical/figures/fig4_worst_errors.png)

## 7. From notebook to browser demo

The trained baseline is also served as a browser demo at <https://iressa-sarcoma-triage-demo.static.hf.space/>, so a reviewer can watch the model run on a slide without installing anything. `demo/export_model.py` exports the same frozen ResNet50 to ONNX (opset 17), quantises it to 8-bit integers (23.7 MB), and writes the scaler and logistic coefficients fitted on all 60 patients to `head.json`. The page runs the identical pipeline in JavaScript with onnxruntime-web: tile at 224 px, keep tiles with at least 40 per cent tissue, extract features, average, apply the logistic head. The image never leaves the machine it is opened on. Quantisation shifts probabilities by a few hundredths compared with the notebook.

The demo shows what the surgeon or pathologist sees: the two subtype probabilities, the first test the model would order, and a low-confidence flag when the top probability is below 0.60, in which case the case follows the standard pathway.

## 8. Limitations and the production model

**Limitations, stated plainly.**

1. Sixty patients and two subtypes. This proves the pipeline runs end to end on open data. It is not a clinical result.
2. Overview resolution only, roughly 16 times downsampled from the scan. Nuclear detail is invisible.
3. Smallest-file selection bias. The sixty slides are the smallest per class, which may favour smaller or less complex tumours.
4. A single scanning programme (TCGA). Stain and scanner variation between hospitals is untested.
5. Mean pooling. Informative regions are averaged with uninformative ones, which is exactly what section 6 shows.

**What changes in the production model.** The table maps each limitation to the change that removes it.

| Baseline (this notebook) | Production model |
|---|---|
| Overview, lowest pyramid level | Full-resolution tiles at 20x |
| Frozen ImageNet ResNet50 | Pathology foundation model (UNI or TITAN) |
| Mean pooling | Attention pooling, multiple-instance learning |
| 60 TCGA patients, 2 subtypes | Multi-hospital cohort, fusion-defined subtypes included |
| Cross-validation only | External validation on held-out hospitals, calibration, subgroup audit |

The multi-hospital validation set and the robustness gate before any clinical use are described in the business case.
**Reporting standard.** The baseline is reported against the items of TRIPOD+AI, the 2024 reporting guideline for prediction models that use machine learning ([Collins and colleagues, BMJ 2024](https://doi.org/10.1136/bmj-2023-078378)): data source and eligibility (section 2), predictors and outcome (sections 3 to 5), sample size and its limits (section 8), model building and internal validation (section 5), performance with calibration not yet assessed, and the fairness items not yet assessable on sixty TCGA patients. A completed TRIPOD+AI checklist will accompany the production model, not this prototype.

