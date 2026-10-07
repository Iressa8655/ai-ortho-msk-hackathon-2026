"""產生 07_fourth_class_and_resolution.ipynb。

  §2 第四類 myxofibrosarcoma，四分類（下載 30 張最低層）
  §3 高一層解析度：同樣 60 個病人，讀金字塔倒數第二層（約 16 倍像素），
     tile 數從幾十變幾百，同一個 pipeline，看 AUC 有沒有變。
下載和特徵都有快取。
"""

import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip()))


def code(text):
    cells.append(nbf.v4.new_code_cell(text.strip()))


md(r"""
# 07 · A fourth class, and one level up in resolution

**Why this notebook exists.** Two limitations of the baseline can only be
tested with more pixels or more patients: resolution (limitation 2 in the
technical report) and the number of subtypes. This notebook downloads what is
needed from the open GDC portal and runs the identical pipeline.

| § | Question | What is downloaded |
|---|---|---|
| 2 | Four classes instead of three | 30 myxofibrosarcoma (MFS) patients, lowest level |
| 3 | Does one level more resolution help | the same 60 LMS and DDLPS patients, the pyramid level above the overview, about 16 times the pixels |
""")

md(r"""
## 1 · Setup

**Story.** Same pipeline as notebooks 01 and 05, copied so this notebook
stands alone; tile features are cached per slide and per level.
""")
code(r"""
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torchvision
import matplotlib.pyplot as plt
from PIL import Image
from tqdm.auto import tqdm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

import fetch_overviews as fo

Image.MAX_IMAGE_PIXELS = None          # level 1 影像約 7000 x 6000，關掉 PIL 的炸彈保護
SEED = 42
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
HERE = Path.cwd(); DATA = HERE / "data"; FIG = HERE / "figures"
OVERVIEWS = DATA / "overviews"; LEVEL1 = DATA / "overviews_level1"
FEAT_DIR = DATA / "features_by_case"; FEAT_DIR.mkdir(exist_ok=True)
TILE, MIN_TISSUE = 224, 0.40

weights = torchvision.models.ResNet50_Weights.IMAGENET1K_V2
backbone = torchvision.models.resnet50(weights=weights)
backbone.fc = torch.nn.Identity(); backbone = backbone.eval()
preprocess = weights.transforms()


def tissue_tiles(png_path):
    img = np.asarray(Image.open(png_path).convert("RGB")); h, w, _ = img.shape; grey = img.mean(axis=2)
    return [img[yy:yy + TILE, xx:xx + TILE]
            for yy in range(0, h - TILE + 1, TILE) for xx in range(0, w - TILE + 1, TILE)
            if (grey[yy:yy + TILE, xx:xx + TILE] < 220).mean() >= MIN_TISSUE]


@torch.no_grad()
def slide_feature(png_path, tag="", batch=32):
    cache = FEAT_DIR / (Path(png_path).stem + tag + ".npy")
    if cache.exists():
        vec = np.load(cache)
        if vec.shape[0] == 2048:              # notebook 05 存的舊格式沒有 tile 數
            vec = np.concatenate([vec, [np.nan]])
        return vec
    tiles = tissue_tiles(png_path)
    if len(tiles) < 3:
        return None
    feats = []
    for s in range(0, len(tiles), batch):
        feats.append(backbone(torch.stack([preprocess(Image.fromarray(t)) for t in tiles[s:s + batch]])))
    vec = np.concatenate([torch.cat(feats).mean(dim=0).numpy(), [len(tiles)]])   # 最後一格存 tile 數
    np.save(cache, vec)
    return vec


def make_model():
    return make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=4000, random_state=SEED))


def features_for(cohort, tag=""):
    X, n_tiles, keep = [], [], []
    for row in tqdm(cohort.itertuples(), total=len(cohort), desc="features" + tag):
        vec = slide_feature(row.png, tag)
        if vec is not None:
            X.append(vec[:-1]); n_tiles.append(int(vec[-1]) if np.isfinite(vec[-1]) else -1); keep.append(row.Index)
    out = cohort.loc[keep].reset_index(drop=True); out["n_tiles"] = n_tiles
    return np.stack(X), out


def oof_binary(X, y, seed=SEED):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed); out = np.zeros(len(y))
    for tr, te in cv.split(X, y):
        out[te] = make_model().fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
    return out


def bootstrap_ci(y, p, n=2000):
    rng = np.random.default_rng(SEED); vals = []
    for _ in range(n):
        idx = rng.integers(0, len(y), len(y))
        if y[idx].min() != y[idx].max():
            vals.append(roc_auc_score(y[idx], p[idx]))
    return np.percentile(vals, [2.5, 97.5])


slides = pd.read_csv(DATA / "tcga_sarc_slides_all.csv")
smallest = pd.read_csv(DATA / "cohort.csv")
feats = np.load(DATA / "slide_features.npz", allow_pickle=True)
base = smallest.set_index("case").loc[list(feats["cases"])].reset_index()
print("baseline cohort", len(base), "slides listed", len(slides))
""")
md(r"""
**Output.** Cohort and slide list loaded; model ready on CPU.
""")

md(r"""
## 2 · Four classes: adding myxofibrosarcoma

**Story.** Myxofibrosarcoma is the second most common soft tissue sarcoma of
the elderly and, like UPS, has no single defining molecular event. Thirty
smallest-file MFS patients are added to the LMS, DDLPS and UPS cohorts from
notebook 05, and the four-class logistic regression is cross-validated.
""")
code(r"""
mfs = slides[slides["diagnosis"] == "Fibromyxosarcoma"].copy()     # GDC 的名稱，就是 myxofibrosarcoma
mfs["label"] = "MFS"
mfs = mfs.sort_values("file_size_mb").drop_duplicates("case").head(30).reset_index(drop=True)
mfs = fo.fetch_cohort(mfs, OVERVIEWS)
X_m, mfs = features_for(mfs)

ups_png = sorted(OVERVIEWS.glob("*_UPS.png"))
ups = pd.DataFrame({"case": [p.stem.replace("_UPS", "") for p in ups_png], "label": "UPS", "png": [str(p) for p in ups_png]})
X_u, ups = features_for(ups)

classes = ["LMS", "DDLPS", "UPS", "MFS"]
X4 = np.vstack([feats["X"], X_u, X_m])
labels4 = np.array(list(base["label"]) + ["UPS"] * len(ups) + ["MFS"] * len(mfs))
y4 = np.array([classes.index(l) for l in labels4])
print("patients per class:", {c: int((labels4 == c).sum()) for c in classes})

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
oof4 = np.zeros((len(y4), 4))
for tr, te in cv.split(X4, y4):
    oof4[te] = make_model().fit(X4[tr], y4[tr]).predict_proba(X4[te])
for k, name in enumerate(classes):
    print(f"{name:6s} one-vs-rest AUC {roc_auc_score(y4 == k, oof4[:, k]):.3f}")
macro4 = np.mean([roc_auc_score(y4 == k, oof4[:, k]) for k in range(4)])
acc4 = (oof4.argmax(1) == y4).mean()
print(f"macro AUC {macro4:.3f}, accuracy {acc4:.2f} (chance 0.25), n = {len(y4)}")

cm = confusion_matrix(y4, oof4.argmax(1))
fig, ax = plt.subplots(figsize=(4.8, 4.5)); ax.imshow(cm, cmap="Blues")
for i in range(4):
    for j in range(4):
        ax.text(j, i, cm[i, j], ha="center", va="center", color="white" if cm[i, j] > cm.max() / 2 else "black")
ax.set_xticks(range(4)); ax.set_xticklabels(classes); ax.set_yticks(range(4)); ax.set_yticklabels(classes)
ax.set_xlabel("Predicted"); ax.set_ylabel("True"); ax.set_title(f"Four classes, out-of-fold, macro AUC {macro4:.2f}")
plt.tight_layout(); plt.savefig(FIG / "fig15_four_class_confusion.png", dpi=120); plt.show()
""")
md(r"""
**Output.** Figure 15 and four one-versus-rest AUCs. MFS and UPS are
expected to be confused with each other most, because both are pleomorphic
and myxoid areas are a matter of degree.
""")

md(r"""
## 3 · One pyramid level up

**Story.** The baseline reads the lowest pyramid level, roughly 2,000 pixels
across. The level above is 4 times larger in each direction, so a slide
yields hundreds of tiles instead of tens and nuclear texture starts to be
visible. Same 60 patients, same pipeline, more pixels. If the AUC rises, the
production plan's move to full resolution is supported; if it does not, the
overview already carries most of the subtype signal at this scale.
""")
code(r"""
level1 = base[["file_id", "file_name", "file_size_mb", "case", "diagnosis", "label"]].copy()
level1 = fo.fetch_cohort(level1, LEVEL1, level_from_end=2)       # 每張約 10 到 100 MB，有快取
level1.to_csv(DATA / "cohort_level1.csv", index=False)
X_l1, level1 = features_for(level1, tag="_level1")
y_l1 = (level1["label"] == "DDLPS").astype(int).to_numpy()
print("tiles per slide at level 1: median", int(level1["n_tiles"].median()), "range", int(level1["n_tiles"].min()), "to", int(level1["n_tiles"].max()))

oof_l1 = oof_binary(X_l1, y_l1); auc_l1 = roc_auc_score(y_l1, oof_l1); ci_l1 = bootstrap_ci(y_l1, oof_l1)
y_b = (base["label"] == "DDLPS").astype(int).to_numpy()
oof_b = oof_binary(feats["X"], y_b); auc_b = roc_auc_score(y_b, oof_b); ci_b = bootstrap_ci(y_b, oof_b)
print(f"lowest level (overview): AUC {auc_b:.3f}, 95% CI {ci_b[0]:.2f} to {ci_b[1]:.2f}")
print(f"one level up:            AUC {auc_l1:.3f}, 95% CI {ci_l1[0]:.2f} to {ci_l1[1]:.2f}, n = {len(y_l1)}")

fig, ax = plt.subplots(figsize=(5.5, 3))
for i, (name, auc, ci) in enumerate([("Lowest level, tens of tiles", auc_b, ci_b), ("One level up, hundreds of tiles", auc_l1, ci_l1)]):
    ax.errorbar(auc, i, xerr=[[auc - ci[0]], [ci[1] - auc]], fmt="o", color="#1f5fbf", capsize=4)
    ax.text(0.5, i + 0.18, name, fontsize=9)
ax.set_yticks([]); ax.set_xlim(0.5, 1.0); ax.axvline(0.5, color="#9aa7ba", ls="--")
ax.set_xlabel("Out-of-fold AUC with 95% bootstrap interval"); ax.set_title("Resolution check, same 60 patients")
plt.tight_layout(); plt.savefig(FIG / "fig16_resolution.png", dpi=120); plt.show()
""")
md(r"""
**Output.** Figure 16. Two intervals, same patients, sixteen times the
pixels in the second. Whatever the direction, the number goes into the
technical report as it is.

## 4 · Summary

Written into the technical report, section 10, after the run.
""")

nb["cells"] = cells
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, "07_fourth_class_and_resolution.ipynb")
print("written", len(cells), "cells")
