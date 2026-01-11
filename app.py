import streamlit as st
import requests
from PIL import Image
import io

# 1. API Configuration
API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"

# 2. Token Security (Secrets se uthayega)
try:
    # Code yahan 'HF_TOKEN' naam dhoondh raha hai
    HF_TOKEN = st.secrets["HF_TOKEN"]
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
except:
    st.error("Secrets box mein 'HF_TOKEN = ...' sahi se nahi likha hai!")
    st.stop()

st.title("⚡ ChattyFroggy Turbo AI")
st.write("Ab background remove hoga sirf 3 seconds mein!")

upload = st.file_uploader("Apni Photo Upload karein", type=["jpg", "png", "jpeg"])

if upload:
    st.image(upload, caption="Original Photo", width=300)
    
    if st.button("Magic Turbo Remove ✨"):
        with st.spinner("AI processing kar raha hai..."):
            try:
                # API ko image bhejna
                response = requests.post(API_URL, headers=headers, data=upload.getvalue())
                
                if response.status_code == 200:
                    st.image(response.content, caption="Turbo Result")
                    st.download_button("Download PNG", response.content, "froggy_no_bg.png")
                elif response.status_code == 503:
                    st.warning("AI Model thoda 'busy' hai, 15-20 seconds mein phir se try karein.")
                elif response.status_code == 401:
                    st.error("Token galat hai! Dubara Secrets check karein.")
                else:
                    st.error(f"Error Code: {response.status_code}")
            except Exception as e:
                st.error("Network issue! Dubara koshish karein.")
