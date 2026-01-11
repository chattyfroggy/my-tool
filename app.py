import streamlit as st
import requests
import io
from PIL import Image

# Token ko clean karne ke liye .strip() lagaya hai
HF_TOKEN = "Hf_wFRJVbvSfCLbAFdVtMCGtHxrdlEVgBarSR".strip()
API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.title("⚡ Turbo AI Fixer")

upload = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if upload:
    if st.button("Magic Remove ✨"):
        with st.spinner("AI Server se connect ho raha hai..."):
            response = requests.post(API_URL, headers=headers, data=upload.getvalue())
            
            if response.status_code == 200:
                st.image(response.content, caption="Success!")
            elif response.status_code == 401:
                st.error("❌ Token Invalid hai! Hugging Face par naya token banayein.")
            elif response.status_code == 503:
                st.warning("⏳ AI Model load ho raha hai... 20 second baad phir try karein.")
            else:
                st.error(f"Error Code: {response.status_code} - {response.text}")
