import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import fitz
import tempfile
import easyocr
import json
from streamlit.components.v1 import html as st_html

def copy_to_clipboard_button(text: str, key: str, label: str = "Copy to Clipboard"):
    payload = json.dumps(text)
    st_html(f"""
        <button id="{key}" style="
            background-color:#232429;
            color:white;
            border:none;
            border-radius:20px;
            padding:8px 20px;
            margin:10px 6px 10 10;
            cursor:pointer;
            font-size:15px;
            display:inline-block;">
            {label}
        </button>
        <script>
        const btn = document.getElementById("{key}");
        btn.addEventListener("click", async () => {{
            try {{
                await navigator.clipboard.writeText({payload});
                btn.innerText = "✅ Copied!";
                setTimeout(() => btn.innerText = "{label}", 2000);
            }} catch (e) {{
                // Fallback for older browsers
                const ta = document.createElement('textarea');
                ta.value = {payload};
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
                btn.innerText = "✅ Copied!";
                setTimeout(() => btn.innerText = "{label}", 2000);
            }}
        }});
        </script>
    """, height=46)

LANG_CHOICES = {
    "en": "English",
    "tl": "Filipino (Tagalog)",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "sv": "Swedish",
    "no": "Norwegian",
    "da": "Danish",
    "fi": "Finnish",
    "cs": "Czech",
    "pl": "Polish",
    "sk": "Slovak",
    "sl": "Slovene",
    "hu": "Hungarian",
    "ro": "Romanian",
    "tr": "Turkish",
    "id": "Indonesian",
    "ms": "Malay",
    "vi": "Vietnamese",
    "ru": "Russian",
    "uk": "Ukrainian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh_sim": "Chinese (Simplified)",
    "zh_traditional": "Chinese (Traditional)",
    "ar": "Arabic",
    "fa": "Persian (Farsi)",
    "he": "Hebrew",
}

st.set_page_config(page_title="Image/PDF to Text", page_icon="📝", layout="wide")

@st.cache_resource(show_spinner=True)
def load_reader(langs):
    return easyocr.Reader(langs, gpu=False)

def pil_draw_boxes(pil_img, results, show_labels=True):
    img = pil_img.copy()
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
    for (bbox, text, conf) in results:
        x_coords = [p[0] for p in bbox]
        y_coords = [p[1] for p in bbox]
        x1, y1, x3, y3 = min(x_coords), min(y_coords), max(x_coords), max(y_coords)
        draw.rectangle([x1, y1, x3, y3], outline="red", width=2)
        if show_labels:
            label = f"{text} ({conf:.2f})"
            tw, th = draw.textbbox((0,0), label, font=font)[2:]
            draw.rectangle([x1, y1 - th - 4, x1 + tw + 6, y1], fill="red")
            draw.text((x1 + 3, y1 - th - 3), label, fill="white", font=font)
    return img

def ocr_image(reader, pil_img):
    arr = np.array(pil_img.convert("RGB"))
    results = reader.readtext(arr)
    text_lines = [r[1] for r in results]
    return results, "\n".join(text_lines)

def pdf_to_images(file_bytes, dpi=180):
    """Convert PDF bytes to list of PIL images using PyMuPDF."""
    images = []
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page_index in range(len(doc)):
            page = doc[page_index]
            zoom = dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append((page_index + 1, img))
    return images

st.title("📝 Image/PDF → Text")
st.write("Upload an image or a PDF. Choose languages, then extract text.")

with st.sidebar:
    st.header("Settings")
    options = list(LANG_CHOICES.keys())
    langs = st.multiselect(
        "Languages",
        options=options,
        default=["en", "tl"],
        format_func=lambda code: f"{code} — {LANG_CHOICES.get(code, code)}",
        help="Pick the languages you expect to see. Fewer languages = faster.",
    )

uploaded = st.file_uploader(
    "Upload image or PDF", 
    type=["png","jpg","jpeg","bmp","tiff","tif","pdf"], 
    accept_multiple_files=False,
    key="file_up"
)

col_run, col_clear = st.columns([1,1])
run_clicked = col_run.button("▶️ Run OCR", type="primary", use_container_width=True)
clear_clicked = col_clear.button("🧹 Clear", use_container_width=True)

if clear_clicked:
    st.session_state.pop("file_up", None)
    st.rerun()

if run_clicked and uploaded is None:
    st.warning("Please upload an image or a PDF first.")

if uploaded and (run_clicked or uploaded.type == "application/pdf"):
    reader = load_reader(langs)

    if uploaded.type == "application/pdf" or uploaded.name.lower().endswith(".pdf"):
        file_bytes = uploaded.read()
        with st.spinner("Converting PDF pages to images…"):
            pages = pdf_to_images(file_bytes)
            st.write(f"PDF has **{len(pages)}** page(s).")

        all_text = []
        for page_num, pil_img in pages:
            with st.spinner(f"OCR on page {page_num}…"):
                results, text = ocr_image(reader, pil_img)
                text = " ".join(text.split())
                all_text.append(f"=== Page {page_num} ===\n{text}")
                # Commented out image display and detected regions
                # if show_boxes:
                #     boxed = pil_draw_boxes(pil_img, results)
                #     st.image(boxed, caption=f"Page {page_num}", use_container_width=True)
                # if results:
                #     st.write(f"**Detected {len(results)} text region(s) on page {page_num}:**")
                #     for (bbox, txt, conf) in results:
                #         st.write(f"- `{txt}` (conf: {conf:.3f})")

        final_text = "\n\n".join(all_text)
        final_text = " ".join(final_text.split())

        st.subheader("Extracted Text")
        st.text_area("Text", final_text, height=400)
        copy_to_clipboard_button(final_text, key="copy_pdf")
        st.download_button(
            "💾 Download TXT",
            data=final_text.encode("utf-8"),
            file_name=(uploaded.name.rsplit(".",1)[0] + "_ocr.txt"),
            mime="text/plain",
            use_container_width=True
        )

    else:
        pil_img = Image.open(uploaded).convert("RGB")
        with st.spinner("Running OCR…"):
            results, text = ocr_image(reader, pil_img)
            text = " ".join(text.split())

        # Commented out image display and detected regions
        # left, right = st.columns([1,1], gap="large")
        # with left:
        #     if show_boxes:
        #         boxed = pil_draw_boxes(pil_img, results)
        #         st.image(boxed, caption="OCR with bounding boxes", use_container_width=True)
        #     else:
        #         st.image(pil_img, caption="Uploaded image", use_container_width=True)

        st.subheader("Extracted Text")
        st.text_area("Text", text, height=400)
        copy_to_clipboard_button(text, key="copy_img")
        st.download_button(
            "💾 Download TXT",
            data=text.encode("utf-8"),
            file_name=(uploaded.name.rsplit(".",1)[0] + "_ocr.txt"),
            mime="text/plain",
            use_container_width=True
        )

        # if results:
        #     st.markdown("**Detected regions:**")
        #     for (bbox, txt, conf) in results:
        #         st.write(f"- `{txt}` (conf: {conf:.3f})")

st.markdown("---")
st.caption("Built with Streamlit + EasyOCR · Supports images and PDFs (via PyMuPDF).")
