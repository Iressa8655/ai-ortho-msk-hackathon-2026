# Technical part: how the baseline model was built

The notebook `01_sarcoma_hne_triage.ipynb` section by section: data, tiling, features, training, errors, the browser demo, limitations, scope, and how to run it.

## 1. Pipeline at a glance

Everything in this section is in one notebook, `technical/01_sarcoma_hne_triage.ipynb`, which runs end to end on a laptop CPU in about an hour, most of it download time. Figure 10 shows the six steps. Each step is one notebook section, with the story above the code, a comment on every line, and the output explained below it.

![The six steps of the baseline, one notebook section each](technical/figures/fig0_pipeline.png)

The design choice behind every step is the same: the smallest thing that proves the overview image carries subtype signal, so that a reviewer can rerun it and get the same number. Nothing is trained from scratch, nothing needs a GPU, and the random seed is fixed at 42 in every notebook. `run_all.py` reruns all seven notebooks in order and prints an MD5 checksum for every figure and data file, so a reviewer can compare a rerun with the submitted outputs line by line (section 10).

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

**What is read.** Only the lowest pyramid level of each slide, fetched over HTTP range requests with `fetch_overviews.py`, about 30 seconds per slide. The whole dataset is sixty small PNG files instead of sixty gigabytes, which is why anyone can rerun the notebook. Figure 11 shows two overviews per class.

![Slide overviews, lowest pyramid level, two per class](technical/figures/fig1_example_overviews.png)

## 3. Tiling and tissue mask

ResNet50 expects 224 px squares, so notebook section 5 slides a 224 px window with no overlap across each overview. A tile is kept only if at least 40 per cent of its pixels are darker than near-white (grey value below 220), which removes glass and most pen marks. Slides with fewer than three tissue tiles would be dropped; none were.

| Class | Slides | Mean tiles | Min | Max |
|---|---|---|---|---|
| DDLPS | 30 | 70.5 | 3 | 129 |
| LMS | 30 | 48.1 | 6 | 105 |

DDLPS slides give more tiles because the tumours are larger and fattier. The count itself cannot leak into the classifier, because the next step averages all tiles into one vector per slide (Figure 12).

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

The 95 per cent bootstrap interval on the out-of-fold AUC is 0.70 to 0.92, and the AUC across 20 different fold assignments ranges from 0.77 to 0.88 (section 9). At a 0.5 threshold 42 of 60 patients are correct, nine errors in each class (Figure 13). The spread between folds, 0.61 to 1.00, is what twelve-patient test folds look like. It is a limit of the cohort size, not a bug.

![ROC curve and confusion matrix, out-of-fold](technical/figures/fig3_roc_confusion.png)

## 6. Where it fails

Notebook section 8 ranks the patients by how confidently wrong the model was. All four worst cases are DDLPS slides scored as LMS with p(DDLPS) below 0.08 (Figure 14).

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

![The browser demo after Start analysis: tissue tiles outlined on the slide, subtype probabilities, the panel to order first, and the processing details](business/fig_demo_screenshot.png)

Figure 15 is the demo after one bundled TCGA-SARC slide has been analysed.

## 8. Limitations and the production model

**Limitations, stated plainly.**

1. Sixty patients and two subtypes in the headline model, ninety and three in the extension (section 9). This proves the pipeline runs end to end on open data. It is not a clinical result.
2. Overview resolution only, roughly 16 times downsampled from the scan. Nuclear detail is invisible. One level up changes nothing with the present pooling (section 9), so resolution must be raised together with attention pooling and pathology-trained features, not alone.
3. Smallest-file selection bias. The sixty slides are the smallest per class. A random cohort of the same size gives the same AUC within its interval (section 9), so the bias did not make the result, but it is still a bias in which tumours were seen.
4. A single scanning programme (TCGA). Stain and scanner variation between hospitals is untested.
5. Mean pooling. Informative regions are averaged with uninformative ones, which is exactly what section 6 shows.

**Scope.** The code in `technical/` is a proof of concept on open TCGA-SARC data, built so that any reviewer can rerun it on a laptop and get the same numbers. It shows that the H&E image alone separates common sarcoma subtypes. The production model is a larger version of the same pipeline, not a different product: moving to it changes the data and the model, not where the tool sits in the pathway or who acts on its output. The table maps each limitation to the change that removes it.

| Baseline (this notebook) | Production model |
|---|---|
| Overview, lowest pyramid level | Full-resolution tiles at 20x |
| Frozen ImageNet ResNet50 | Pathology foundation model (UNI or TITAN) |
| Mean pooling | Attention pooling, multiple-instance learning |
| 60 TCGA patients, 2 subtypes | Multi-hospital cohort, fusion-defined subtypes included |
| Cross-validation only | External validation on held-out hospitals, calibration, subgroup audit |

The multi-hospital validation set and the robustness gate before any clinical use are described in the business case.
**Reporting standard.** The baseline is reported against the items of TRIPOD+AI, the 2024 reporting guideline for prediction models that use machine learning ([Collins and colleagues, BMJ 2024](https://doi.org/10.1136/bmj-2023-078378)): data source and eligibility (section 2), predictors and outcome (sections 3 to 5), sample size and its limits (section 8), model building and internal validation (section 5), performance, uncertainty, calibration and robustness (section 9), and the fairness items not yet assessable on sixty TCGA patients. A completed TRIPOD+AI checklist will accompany the production model, not this prototype.

## 9. Robustness checks

One number, AUC 0.82 on 60 patients, invites eight questions about the data and five about the modelling. Notebook `technical/03_robustness_checks.ipynb` answers the first six with the cached features from notebook 01 and runs in minutes on a CPU; notebooks `05_more_data_checks.ipynb` and `07_fourth_class_and_resolution.ipynb` download more slides for the rest. All numbers below are from that run (seed 42).


**Highlights for the data scientist.** AUC 0.82 with a 95 per cent bootstrap interval of 0.70 to 0.92; a permutation null with p = 0.002; stable across 20 fold assignments; Macenko stain normalisation lifts the point estimate to 0.86; the result survives a random cohort and a third and fourth subtype; one level more resolution adds nothing with mean pooling; every number is out-of-fold and reproducible from `run_all.py`.

| Question | Method | Result |
|---|---|---|
| How wide is the error on 0.82 | Bootstrap, 2,000 resamples of the 60 patients | 95 per cent interval **0.70 to 0.92** |
| Was the split lucky | 5-fold cross-validation repeated with 20 seeds | mean 0.81, range 0.77 to 0.88; seed 42 is typical |
| Could 60 patients give 0.8 by chance | Permutation null, 500 label shuffles | null mean 0.50, 95th percentile 0.65; real 0.82, **p = 0.002** |
| Are the probabilities calibrated | Reliability diagram, 5 bins, Brier score | Brier **0.21**; mild under-confidence in the middle bins (Figure 17) |
| Colour or tissue | Hue, saturation and brightness perturbation, out-of-fold scoring | 2 to 4 of 60 calls flip; AUC 0.78 to 0.83 against 0.82 unperturbed |
| Did the smallest-file shortcut make the result | 30 + 30 patients drawn at random instead of the 30 smallest files per class, notebook 05 | AUC **0.81** (0.69 to 0.91) against 0.82 (0.70 to 0.92); 36 of the 60 patients overlap, because many patients only have one small slide |
| Does a third, harder class break it | 30 undifferentiated pleomorphic sarcoma (UPS) patients added, three-class logistic regression, notebook 05 | macro one-versus-rest AUC **0.83** on 90 patients (LMS 0.82, DDLPS 0.83, UPS 0.83), accuracy 0.67 against 0.33 chance (Figure 20) |
| Does a fourth class break it | 20 myxofibrosarcoma (MFS) patients added (10 of the 30 smallest files had too little tissue), four-class logistic regression, notebook 07 | macro one-versus-rest AUC **0.77** on 110 patients (LMS 0.81, DDLPS 0.82, UPS 0.73, MFS 0.73), accuracy 0.52 against 0.25 chance (Figure 24) |
| Does one level more resolution help | The same 60 patients read one pyramid level up, 16 times the pixels, median 276 tiles per slide instead of 57, notebook 07 | AUC **0.83** (0.72 to 0.93) against 0.82 (0.70 to 0.92): no measurable gain at this scale (Figure 25) |
| Where does it look | Tile-level probability maps, leave-one-patient-out head | the four worst DDLPS slides are a mix of red and blue tiles; the mean dilutes the DDLPS signal (Figure 18) |

![Permutation null from 500 label shuffles; the real AUC sits outside it](technical/figures/fig6_permutation_null.png)

**What the interval means.** The data support "clearly above chance", not "0.82". The honest headline is 0.82 (95 per cent interval 0.70 to 0.92), and the permutation test (Figure 16) rules out a chance result with 60 patients and 2,048 features.

![Reliability diagram, five quantile bins, Brier score 0.21](technical/figures/fig7_calibration.png)

**Calibration.** The head is strongly regularised (C = 0.1), so probabilities are pulled toward 0.5 and the curve is slightly under-confident in the middle. For triage this is the safer direction: a 0.6 means at least 0.6. Calibration will be refitted on the production cohort, where the abstain threshold is set.

**Stain and scanner.** The synthetic perturbations shift the mean probability by 0.03 to 0.07 and flip at most 4 of 60 calls; brightening is the most damaging (AUC 0.78). At overview resolution the features are mostly tissue-driven, but this is a synthetic test, not real inter-laboratory variation. The 30-hospital, 3-scanner dataset in the business case is the real gate, and the published sarcoma foundation-model result that falls from 0.94 to 0.47 across institutions is why that gate exists.

![The four most confident errors, overview above and tile-level p(DDLPS) below, scored by a head that never saw that patient](technical/figures/fig8_tile_maps.png)

**Where it looks.** Scored tile by tile, the four worst DDLPS slides contain many DDLPS-like tiles (17 to 47 of 31 to 86 tiles above 0.5) next to large LMS-like regions. Averaging the features before classification lets the larger region win. This is the mean-pooling failure named in section 6 and the reason the production model uses attention pooling.

![Selection bias check: the smallest-file cohort and a random cohort give overlapping intervals](technical/figures/fig10_random_vs_smallest.png)

**Random patients instead of the smallest files.** The random cohort's files are 10 to 20 times larger on average (LMS mean 1,147 MB, DDLPS 1,559 MB, against 72 to 250 MB for the smallest), yet the out-of-fold AUC is 0.81 (0.69 to 0.91) against 0.82 (0.70 to 0.92) (Figure 19). The shortcut did not make the result. The overlap of 36 patients is a property of TCGA-SARC, where most patients have a single slide, so the two cohorts cannot be fully disjoint at 30 per class.

![Three classes, out-of-fold confusion matrix, 90 patients](technical/figures/fig11_three_class_confusion.png)

**A third class.** With UPS added, a diagnosis of exclusion with no defining molecular event, the three-class model keeps a macro one-versus-rest AUC of 0.83 on 90 patients and two thirds of patients are called correctly at the top probability (Figure 20). The overview carries subtype signal beyond the easiest pair. Fusion-defined subtypes remain out of reach on open data because too few slides exist, which is the reason for the RNOH and Taiwan cohorts.

**Modelling variants on the same 60 overviews.** Notebook `06_second_round_checks.ipynb` asks whether the modelling choices were the right ones. Every row is out-of-fold on the same folds with a bootstrap interval (Figure 21).

| Variant | AUC | 95 per cent interval | Reading |
|---|---|---|---|
| Mean pool + logistic regression (baseline) | 0.82 | 0.70 to 0.92 | reference |
| k-nearest neighbours, k = 7 | 0.82 | 0.70 to 0.92 | same |
| Random forest, 500 trees | 0.76 | 0.62 to 0.88 | lower |
| Linear SVM | 0.75 | 0.61 to 0.87 | lower |
| RBF SVM | 0.71 | 0.57 to 0.84 | lower |
| Gated attention MIL over tiles | 0.70 | 0.56 to 0.83 | lower; 48 training slides are too few to learn attention weights, so this does not test the production design, which rests on far more slides |
| Phikon pathology foundation model features + logistic | 0.80 | 0.67 to 0.90 | same; at overview resolution the pathology-pretrained features ([Filiot and colleagues 2023](https://doi.org/10.1101/2023.07.21.23292757)) do not beat ImageNet, which is expected because Phikon was trained on 20x tiles, not overviews |
| Macenko stain normalisation + baseline | 0.86 | 0.75 to 0.96 | highest point estimate, interval overlaps the baseline |

![Every modelling variant with its interval; the baseline was not a careless choice](technical/figures/fig14_variants.png)

**Learning curve.** Training on 16, 24, 32 and 40 patients gives mean AUCs of 0.77, 0.80, 0.82 and 0.83 over 30 random draws (Figure 22); at 48 the held-out set is only 12 patients and the estimate becomes too noisy to read. The curve is still rising at 40. More patients are worth more than any change of classifier, which is the case for the RNOH and Taiwan cohorts.

![Learning curve, mean AUC over 30 random draws per training size](technical/figures/fig12_learning_curve.png)

**Stain normalisation.** Macenko normalisation ([Macenko and colleagues 2009](https://doi.org/10.1109/ISBI.2009.5193250)) applied to every overview before feature extraction gives the highest point estimate of any variant, 0.86, with an interval that overlaps the baseline (Figure 23 shows one overview before and after). It costs nothing at inference and addresses the first risk in the business case directly, so it goes into the production pipeline; the 30-hospital dataset will say whether the gain is real.

![One overview before and after Macenko normalisation](technical/figures/fig13_macenko_example.png)

![Four classes, out-of-fold confusion matrix, 110 patients](technical/figures/fig15_four_class_confusion.png)

**A fourth class.** Adding myxofibrosarcoma lowers the macro AUC from 0.83 to 0.77 and the accuracy from 0.67 to 0.52 (Figure 24). The two fusion-free, pleomorphic subtypes, UPS and MFS, are the ones confused, each at 0.73 one-versus-rest, while LMS and DDLPS hold at 0.81 and 0.82. That is the expected shape: the subtypes without a defining molecular event are also the ones without a defining low-resolution appearance. Only 20 of the 30 smallest MFS files had three or more tissue tiles at overview resolution, which is itself a limit of the overview shortcut.

![Resolution check: the same 60 patients at the overview level and one level up](technical/figures/fig16_resolution.png)

**One level up in resolution.** Reading the pyramid level above the overview gives sixteen times the pixels and a median of 276 tissue tiles per slide instead of 57, yet the out-of-fold AUC moves from 0.82 to 0.83 with overlapping intervals (Figure 25). With mean pooling and a frozen ImageNet backbone, more tiles of the same kind add little; the gain from resolution is expected to come only when the pooling can weight tiles and the features are pathology-trained, which is why the production plan changes those two things together rather than resolution alone. The 60 level-1 images total 4 GB and took about half an hour to fetch, against a few megabytes for the overviews, which is why the baseline reads overviews.

## 10. How to run


```
conda create -n sarc python=3.12
pip install -r technical/requirements.txt
cd technical
jupyter lab 01_sarcoma_hne_triage.ipynb # run all, first run downloads ~60 overviews
jupyter lab 02_savings_model.ipynb
jupyter lab 03_robustness_checks.ipynb # uses the cache from 01, minutes on CPU
jupyter lab 04_competitor_landscape.ipynb # live PubMed counts, about one minute
jupyter lab 05_more_data_checks.ipynb # downloads about 60 more overviews
jupyter lab 06_second_round_checks.ipynb # learning curve, heads, attention MIL, Phikon, Macenko; Phikon weights download once
jupyter lab 07_fourth_class_and_resolution.ipynb # 30 MFS overviews and the 60 level-1 images, about two hours of download

# or everything in one go, with MD5 checksums of every output at the end
python run_all.py
python run_all.py --check # checksums only, no execution
```

To see the trained baseline run on a slide, open the live demo at <https://iressa-sarcoma-triage-demo.static.hf.space/> (hosted as a Hugging Face Space; the model runs in your browser and the image never leaves your machine), or run it locally:

```
cd demo
python -m http.server 8765
```

Then open <http://localhost:8765/>, drop an H&E overview image or click one of the six bundled TCGA-SARC slides. The model runs in the browser in a few seconds and shows the subtype probabilities and the panel it would order first. `demo/README.md` explains the files.

Seed 42 is fixed in every notebook. `requirements-lock.txt` lists the exact package versions of the submitted run, and `run_all.py --check` prints the MD5 of every figure and data file so a rerun can be compared line by line. Features and overviews are cached under `technical/data/` after the first run.

