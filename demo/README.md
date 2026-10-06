# Sarcoma H&E triage demo

A browser-only demo of the hackathon baseline model. Upload an H&E overview image, or click one of six real TCGA-SARC slides, and the model runs on your machine and returns a subtype probability in a few seconds.

What runs: the exact pipeline of `technical/01_sarcoma_hne_triage.ipynb`. The overview is cut into 224 px tiles, tiles with at least 40 per cent tissue go through a frozen ImageNet ResNet50 (exported to ONNX, int8), tile features are averaged, and a logistic regression head fitted on the 60 TCGA-SARC patients gives p(dedifferentiated liposarcoma) versus leiomyosarcoma. The int8 export shifts probabilities by a few hundredths compared with the notebook.

What it does not do yet: say whether the slide is a sarcoma at all, or recognise the fusion-defined subtypes. Those are the production model's tasks (business case §2). This is a proof of concept, not a clinical tool.

## Run locally

```
cd demo
python -m http.server 8765
```

Open <http://localhost:8765/>. Add `?sample=TCGA-3B-A9HL_DDLPS` to the URL to auto-run one bundled slide.

## Files

| Path | What |
|---|---|
| `index.html`, `app.js` | the page and the pipeline, onnxruntime-web from jsDelivr |
| `model/resnet50_int8.onnx` | frozen backbone, 23.7 MB, built by `export_model.py` |
| `model/head.json` | scaler mean and scale, logistic coefficients and intercept |
| `samples/*.jpg` | six TCGA-SARC overviews, three DDLPS and three LMS, from the open GDC portal |
| `export_model.py` | rebuilds `model/` from the notebook's cached features and torchvision weights |

The image never leaves the browser. No server receives it.
