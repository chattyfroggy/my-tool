import streamlit as st
import requests
from PIL import Image
import io

# Naya Model URL
API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"

try:
    # Ye line secrets se HF_TOKEN ko uthayegi
    HF_TOKEN = st.secrets["HF_TOKEN"]
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
except:
    st.error("Secrets mein 'HF_TOKEN' nahi mila! Format check karein.")
    st.stop()

st.title("⚡ ChattyFroggy Turbo Studio")

upload = st.file_uploader("Photo choose karein", type=["jpg", "png", "jpeg"])

if upload:
    st.image(upload, caption="Original Photo", width=300)
    
    if st.button("Magic Turbo Remove ✨"):
        with st.spinner("AI Server se result la raha hoon..."):
            try:
                response = requests.post(API_URL, headers=headers, data=upload.getvalue(), timeout=30)
                
                if response.status_code == 200:
                    st.image(response.content, caption="Success!")
                    st.download_button("Download PNG", response.content, "result.png")
                elif response.status_code == 503:
                    st.warning("Model load ho raha hai, 20-30 seconds baad phir se button dabayein.")
                else:
                    st.error(f"Error {response.status_code}: Token ya model issue hai.")
            except Exception as e:
                st.error("Connection timeout! Dubara koshish karein.")
