// Sarcoma H&E triage demo, runs the hackathon baseline in the browser.
// Pipeline mirrors technical/01_sarcoma_hne_triage.ipynb:
//   overview image → 224 px tiles (≥40 % tissue) → ResNet50 features → mean → logistic head.

const TILE = 224;
const MIN_TISSUE = 0.40;
const MEAN = [0.485, 0.456, 0.406];
const STD = [0.229, 0.224, 0.225];
const SAMPLES = [
  ["TCGA-3B-A9HL", "DDLPS"], ["TCGA-DX-A6BE", "DDLPS"], ["TCGA-3B-A9HI", "DDLPS"],
  ["TCGA-FX-A48G", "LMS"], ["TCGA-3B-A9HY", "LMS"], ["TCGA-MB-A5YA", "LMS"],
];

let session = null;
let head = null;

const $ = (id) => document.getElementById(id);

function setProgress(frac, text) {
  $("progress").style.width = `${Math.round(frac * 100)}%`;
  $("progressText").textContent = text;
}

async function loadModel() {
  if (session) return;
  setProgress(0.05, "loading model (about 25 MB, once)");
  ort.env.wasm.wasmPaths = "https://cdn.jsdelivr.net/npm/onnxruntime-web@1.19.2/dist/";
  const [sess, headJson] = await Promise.all([
    ort.InferenceSession.create("model/resnet50_int8.onnx", { executionProviders: ["wasm"] }),
    fetch("model/head.json").then((r) => r.json()),
  ]);
  session = sess;
  head = headJson;
  setProgress(0.1, "model ready");
}

// Cut the overview into 224 px tiles and keep the ones that are mostly tissue.
function tileImage(img) {
  const canvas = document.createElement("canvas");
  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(img, 0, 0);
  const tiles = [];
  for (let y = 0; y + TILE <= canvas.height; y += TILE) {
    for (let x = 0; x + TILE <= canvas.width; x += TILE) {
      const data = ctx.getImageData(x, y, TILE, TILE).data;
      let tissue = 0;
      for (let i = 0; i < data.length; i += 4) {
        const grey = (data[i] + data[i + 1] + data[i + 2]) / 3;
        if (grey < 220) tissue += 1;
      }
      if (tissue / (TILE * TILE) >= MIN_TISSUE) tiles.push({ x, y, data });
    }
  }
  return tiles;
}

// ImageNet normalisation, NCHW float32.
function toTensor(batch) {
  const n = batch.length;
  const arr = new Float32Array(n * 3 * TILE * TILE);
  batch.forEach((t, b) => {
    for (let i = 0; i < TILE * TILE; i += 1) {
      for (let c = 0; c < 3; c += 1) {
        arr[b * 3 * TILE * TILE + c * TILE * TILE + i] = (t.data[i * 4 + c] / 255 - MEAN[c]) / STD[c];
      }
    }
  });
  return new ort.Tensor("float32", arr, [n, 3, TILE, TILE]);
}

function drawTiles(img, tiles) {
  const cv = $("tiles");
  const rect = img.getBoundingClientRect();
  const parent = $("viewer").getBoundingClientRect();
  cv.width = parent.width;
  cv.height = parent.height;
  const sx = rect.width / img.naturalWidth;
  const sy = rect.height / img.naturalHeight;
  const ox = rect.left - parent.left;
  const oy = rect.top - parent.top;
  const ctx = cv.getContext("2d");
  ctx.clearRect(0, 0, cv.width, cv.height);
  ctx.strokeStyle = "rgba(56,138,221,0.9)";
  ctx.lineWidth = 1;
  tiles.forEach((t) => ctx.strokeRect(ox + t.x * sx, oy + t.y * sy, TILE * sx, TILE * sy));
}

function sigmoid(z) { return 1 / (1 + Math.exp(-z)); }

async function run(img, label) {
  await loadModel();
  const tiles = tileImage(img);
  $("tileInfo").textContent = `Tiles: ${tiles.length} tissue tiles of ${TILE} px`;
  drawTiles(img, tiles);
  if (tiles.length < 3) { setProgress(1, "too little tissue"); return; }

  const BATCH = 8;
  const sum = new Float64Array(2048);
  const t0 = performance.now();
  for (let i = 0; i < tiles.length; i += BATCH) {
    const batch = tiles.slice(i, i + BATCH);
    const out = await session.run({ input: toTensor(batch) });
    const feats = out.features.data;
    for (let b = 0; b < batch.length; b += 1) {
      for (let k = 0; k < 2048; k += 1) sum[k] += feats[b * 2048 + k];
    }
    setProgress(0.1 + 0.9 * Math.min(1, (i + batch.length) / tiles.length), `${Math.min(i + batch.length, tiles.length)} / ${tiles.length} tiles`);
  }
  // mean-pool, standardise, logistic head
  let z = head.intercept;
  for (let k = 0; k < 2048; k += 1) {
    const v = (sum[k] / tiles.length - head.mean[k]) / head.scale[k];
    z += v * head.coef[k];
  }
  const pD = sigmoid(z);
  const pL = 1 - pD;
  $("barD").style.width = `${Math.round(pD * 100)}%`;
  $("barL").style.width = `${Math.round(pL * 100)}%`;
  $("pD").textContent = pD.toFixed(2);
  $("pL").textContent = pL.toFixed(2);
  const secs = ((performance.now() - t0) / 1000).toFixed(1);
  $("timing").textContent = `${secs} s in browser`;
  setProgress(1, "done");

  const top = pD >= 0.5 ? "DDLPS" : "LMS";
  const conf = Math.max(pD, pL);
  $("orderBox").classList.remove("hidden");
  $("orderText").textContent = top === "DDLPS"
    ? "MDM2 amplification (FISH) · dedifferentiated liposarcoma panel"
    : "Smooth-muscle immunohistochemistry · leiomyosarcoma work-up";
  $("orderNote").textContent = label ? `Ground truth for this TCGA slide: ${label}${label === top ? " ✓" : " ✗"}` : "No ground truth for an uploaded image";
  $("abstainBox").classList.toggle("hidden", conf >= 0.60);
}

function showImage(src, name, label) {
  const img = $("slide");
  img.onload = () => { img.classList.remove("hidden"); $("dropzone").classList.add("hidden"); $("caseName").textContent = name; run(img, label); };
  img.src = src;
}

$("file").addEventListener("change", (e) => {
  const f = e.target.files[0];
  if (f) showImage(URL.createObjectURL(f), f.name, null);
});
const viewer = $("viewer");
viewer.addEventListener("dragover", (e) => e.preventDefault());
viewer.addEventListener("drop", (e) => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) showImage(URL.createObjectURL(f), f.name, null); });

SAMPLES.forEach(([c, l]) => {
  const b = document.createElement("button");
  b.className = "bg-slate-700 text-slate-100 text-xs px-3 py-1 rounded hover:bg-slate-600";
  b.textContent = `${c} (${l})`;
  b.onclick = () => showImage(`samples/${c}_${l}.jpg`, `${c} · ${l}`, l);
  $("samples").appendChild(b);
});

// ?sample=TCGA-MB-A5YA_LMS auto-runs one bundled slide, used for screenshots and demos.
const auto = new URLSearchParams(location.search).get("sample");
if (auto) {
  const [c, l] = [auto.replace(/_(LMS|DDLPS)$/, ""), auto.endsWith("DDLPS") ? "DDLPS" : "LMS"];
  showImage(`samples/${auto}.jpg`, `${c} · ${l}`, l);
}
