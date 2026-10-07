# Technical

Seven notebooks, one download helper, one run-all script. Everything runs on a laptop CPU.

| File | What it does |
|---|---|
| `01_sarcoma_hne_triage.ipynb` | Baseline: 60 TCGA-SARC patients, frozen ResNet50 on slide overviews, logistic regression, 5-fold CV, AUC 0.82 |
| `02_savings_model.ipynb` | Savings arithmetic, every input labelled sourced or assumption |
| `03_robustness_checks.ipynb` | Bootstrap interval, 20 seeds, permutation null, calibration, stain perturbation, tile maps |
| `04_competitor_landscape.ipynb` | Live PubMed counts behind the competition figure |
| `05_more_data_checks.ipynb` | Random patients instead of smallest files; a third subtype |
| `06_second_round_checks.ipynb` | Learning curve, other heads, attention MIL, Phikon features, Macenko normalisation |
| `07_fourth_class_and_resolution.ipynb` | A fourth subtype; the same 60 patients one pyramid level up |
| `fetch_overviews.py` | Lists TCGA-SARC slides through the GDC API and reads only the lowest pyramid level over HTTP range requests |
| `build_*_notebook.py` | Generate each notebook from source, so the cells are reviewable as plain Python |
| `run_all.py` | Executes 01 to 07 in order and prints MD5 checksums of every figure and data file (`--check` prints checksums only) |
| `requirements.txt` | Minimum versions |
| `requirements-lock.txt` | Exact versions used for the submitted run |
| `data/` | Slide list, cohorts, cached overviews and features (overviews are not in the zip; the first run downloads them) |
| `figures/` | Every figure in the technical report, numbered |

Seed 42 is fixed in every notebook. Data source: [GDC TCGA-SARC](https://portal.gdc.cancer.gov/projects/TCGA-SARC), open access.
