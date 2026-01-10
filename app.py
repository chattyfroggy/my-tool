import streamlit as st
import requests
from PIL import Image, ImageEnhance
import io
import urllib.parse

# 1. API Setup (Secrets se token uthayega)
API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"
# Agar aap local test kar rahe hain toh yahan token daal sakte hain, 
# par Streamlit Cloud ke liye niche wala 'st.secrets' best hai.
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    HF_TOKEN = "Hf_wFRJVbvSfCLbAFdVtMCGtHxrdlEVgBarSR" # Temporary for local test

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="ChattyFroggy AI Turbo", layout="wide")

# Modern UI CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .stButton>button { 
        background: linear-gradient(90deg, #00dbde 0%, #fc00ff 100%); 
        color: white; border-radius: 25px; font-weight: bold; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ ChattyFroggy AI Turbo Studio")

# Helper to remove background via API
def remove_bg_api(image_bytes):
    response = requests.post(API_URL, headers=headers, data=image_bytes)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"API Error: {response.status_code}")
        return None

upload = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if upload:
    if st.button("Generate Turbo Magic ✨"):
        with st.spinner("AI Servers (Turbo) se connect ho raha hai..."):
            # 1. Background Removal via Turbo API
            result_bytes = remove_bg_api(upload.getvalue())
            
            if result_bytes:
                subject_img = Image.open(io.BytesIO(result_bytes)).convert("RGBA")
                
                # Display Results
                col1, col2 = st.columns(2)
                with col1:
                    st.image(upload, caption="Original", use_container_width=True)
                with col2:
                    st.image(subject_img, caption="Turbo Transparent", use_container_width=True)
                    st.download_button("Download PNG", result_bytes, "turbo_froggy.png", "image/png")
