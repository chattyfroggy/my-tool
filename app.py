import streamlit as st
import requests
from PIL import Image
import io

# API Configuration
API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"

# Secrets se token nikalne ki koshish
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
except:
    st.error("Secrets mein HF_TOKEN missing hai!")
    st.stop()

st.title("⚡ ChattyFroggy Turbo AI")

upload = st.file_uploader("Photo choose karein", type=["jpg", "png", "jpeg"])

if upload:
    st.image(upload, caption="Original", width=250)
    
    if st.button("Magic Turbo Remove ✨"):
        with st.spinner("AI Server se result la raha hoon..."):
            try:
                # Direct API Call
                response = requests.post(API_URL, headers=headers, data=upload.getvalue(), timeout=20)
                
                if response.status_code == 200:
                    st.image(response.content, caption="Turbo Result")
                    st.download_button("Download PNG", response.content, "result.png")
                elif response.status_code == 503:
                    st.warning("AI Model so raha hai (Loading), 30 seconds baad phir button dabayein.")
                else:
                    st.error(f"API Error: {response.status_code}. Token check karein.")
            except Exception as e:
                st.error("Connection slow hai, dobara try karein.")