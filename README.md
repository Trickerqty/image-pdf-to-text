# EasyOCR Image/PDF → Text (Streamlit App)

This project is a **Streamlit web app** that uses [EasyOCR](https://github.com/JaidedAI/EasyOCR) to extract text from **images** and **PDF documents**.  
It supports multiple languages (e.g., English 🇬🇧, Filipino 🇵🇭, Spanish 🇪🇸, etc.) and cleans the extracted text into a straight, continuous paragraph for easier reading or copying.

---

## Features

✅ Upload **images or PDFs**  
✅ Supports 30+ languages (English, Tagalog, Spanish, etc.)  
✅ Outputs clean, line-free text  
✅ Download result as `.txt`  
✅ Fast & deployable on [Streamlit Cloud](https://streamlit.io/cloud)

---

## Tech Stack

| Component | Description |
|------------|-------------|
| **Python** | Core language |
| **Streamlit** | Web interface framework |
| **EasyOCR** | Optical character recognition engine |
| **PyMuPDF (fitz)** | Converts PDF pages to images |
| **Pillow (PIL)** | Image handling |
| **NumPy** | Image array processing |

---

## Setup & Installation

### Clone this repository
```bash
git clone https://github.com/Trickerqty/image-pdf-to-text.git
```
```bash
cd easyocr-streamlit-app
```
### Create and activate a virtual environment
```bash
python -m venv venv
```
# Windows
```bash
venv\Scripts\activate
```

# macOS/Linux
```bash
source venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the app
```bash
streamlit run app.py
```
---

