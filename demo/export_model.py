"""把 notebook 01 的模型匯出給瀏覽器用。

兩個檔：
1. resnet50_int8.onnx  凍住的 ImageNet ResNet50（去掉分類頭），int8 量化，
   瀏覽器用 onnxruntime-web 跑。
2. head.json  在全部 60 個病人上重新 fit 的 StandardScaler + LogisticRegression，
   只存 mean、scale、coef、intercept，瀏覽器用幾行 JS 就能算。

這跟 notebook 的差別只有一個：notebook 用 5-fold 交叉驗證報 AUC，
這裡用全部 60 人 fit 一次當 demo 模型。
"""

import json
from pathlib import Path

import numpy as np
import torch
import torchvision
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
TECH = HERE.parent / "technical"
OUT = HERE / "model"
OUT.mkdir(exist_ok=True)


def export_head():
    """用快取的 60 × 2048 特徵重新 fit 一次，存成 JSON。"""
    cache = np.load(TECH / "data" / "slide_features.npz", allow_pickle=True)
    X, cases = cache["X"], list(cache["cases"])
    import pandas as pd
    cohort = pd.read_csv(TECH / "data" / "cohort.csv")
    labels = dict(zip(cohort["case"], cohort["label"]))
    y = np.array([1 if labels[c] == "DDLPS" else 0 for c in cases])

    scaler = StandardScaler().fit(X)
    clf = LogisticRegression(C=0.1, max_iter=2000, random_state=42)
    clf.fit(scaler.transform(X), y)
    head = {
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist(),
        "coef": clf.coef_[0].tolist(),
        "intercept": float(clf.intercept_[0]),
        "positive_label": "DDLPS",
        "negative_label": "LMS",
        "n_train": int(len(y)),
        "note": "fit on all 60 TCGA-SARC patients; CV AUC 0.82 in notebook 01",
    }
    (OUT / "head.json").write_text(json.dumps(head))
    print("head.json written, train acc",
          round(float(clf.score(scaler.transform(X), y)), 3))


def export_backbone():
    """ResNet50 去頭，匯出 ONNX，再 int8 量化縮到約 25 MB。"""
    weights = torchvision.models.ResNet50_Weights.IMAGENET1K_V2
    model = torchvision.models.resnet50(weights=weights)
    model.fc = torch.nn.Identity()
    model.eval()
    dummy = torch.zeros(1, 3, 224, 224)
    fp32 = OUT / "resnet50_fp32.onnx"
    torch.onnx.export(
        model, dummy, str(fp32),
        input_names=["input"], output_names=["features"],
        dynamic_axes={"input": {0: "batch"}, "features": {0: "batch"}},
        opset_version=17, dynamo=False,
    )
    from onnxruntime.quantization import quantize_dynamic, QuantType
    int8 = OUT / "resnet50_int8.onnx"
    quantize_dynamic(str(fp32), str(int8), weight_type=QuantType.QUInt8)
    print("onnx sizes MB:", round(fp32.stat().st_size / 1e6, 1),
          round(int8.stat().st_size / 1e6, 1))
    fp32.unlink()                          # 只留量化版，fp32 太大不進 repo


if __name__ == "__main__":
    export_head()
    export_backbone()
