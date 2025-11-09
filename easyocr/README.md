
# EasyOCR Image/PDF to Text (Streamlit)

A minimal Streamlit app that uses **EasyOCR** to extract text from images **and PDFs** (via PyMuPDF).  
- Choose OCR languages (e.g., `en`, `tl` for Filipino/Tagalog).  
- Optional bounding boxes and labels with confidence.  
- Download extracted text as `.txt`.

## 1) Run locally

```bash
# 1. Create and activate a virtual env (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch
streamlit run app.py
```

Then open the local URL shown in the terminal.

> **Tip:** The first run downloads OCR models under `~/.EasyOCR`; subsequent runs are faster.

## 2) Deploy on Streamlit Community Cloud

1. Push this folder to a **public GitHub repo**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and deploy your repo.
3. Set the **main file** to `app.py`.
4. (Optional) In **Advanced settings**, increase memory if you handle long PDFs.

## 3) Languages

- Default: `en`, `tl`.  
- Add or remove languages in the sidebar. Fewer languages = faster OCR.  
- See EasyOCR docs for full language list.

## 4) Notes

- **PDFs** are rasterized with **PyMuPDF** at ~180 DPI for better accuracy.
- If you need faster/better accuracy, try adjusting the DPI or pre-processing images (denoise/threshold).
- On some hosts, building `torch` may take time. EasyOCR will install a compatible torch wheel automatically.

## 5) Troubleshooting

- If OCR is slow or memory-heavy on big PDFs, reduce DPI in `pdf_to_images` (e.g., `dpi=120`).
- On Linux servers, prefer `opencv-python-headless` (already in requirements).
- If deployment fails due to `torch` wheel, pin a specific CPU wheel that matches your platform.

## License

MIT
