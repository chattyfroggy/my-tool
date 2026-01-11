import streamlit as st
import requests
from PIL import Image
import io

# NAYA WORKING API URL
API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"

try:
    # Secrets se token uthana
    HF_TOKEN = st.secrets["HF_TOKEN"]
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
except:
    st.error("Secrets mein HF_TOKEN nahi mila! Format check karein: HF_TOKEN = 'your_token'")
    st.stop()

st.title("⚡ ChattyFroggy Turbo Studio")

upload = st.file_uploader("Photo choose karein", type=["jpg", "png", "jpeg"])

if upload:
    st.image(upload, caption="Original Photo", width=300)
    
    if st.button("Magic Turbo Remove ✨"):
        with st.spinner("AI Server se connect ho raha hai..."):
            try:
                # API Call
                response = requests.post(API_URL, headers=headers, data=upload.getvalue(), timeout=30)
                
                if response.status_code == 200:
                    st.image(response.content, caption="Turbo Result")
                    st.download_button("Download PNG", response.content, "froggy_result.png")
                elif response.status_code == 503:
                    # Model loading time (Jag raha hai server)
                    st.warning("Model load ho raha hai (Loading...), 20 seconds baad phir se button click karein.")
                elif response.status_code == 401:
                    st.error("Token Invalid! Naya token banayein.")
                else:
                    st.error(f"Error {response.status_code}: Please try again.")
            except Exception as e:
                st.error("Connection timeout! Dubara koshish karein.")
