import pandas as pd, numpy as np, fetch_overviews as fo
from pathlib import Path
base = pd.read_csv("data/cohort.csv")
feats = np.load("data/slide_features.npz", allow_pickle=True)
base = base.set_index("case").loc[list(feats["cases"])].reset_index()
out = fo.fetch_cohort(base[["file_id","file_name","file_size_mb","case","diagnosis","label"]], Path("data/overviews_level1"), level_from_end=2)
out.to_csv("data/cohort_level1.csv", index=False)
print("LEVEL1 DONE", len(out))
