import streamlit as st
import requests
from PIL import Image, ImageEnhance
import io
import urllib.parse

# Page Configuration
st.set_page_config(page_title="ChattyFroggy AI Turbo Studio", layout="wide")

# Modern UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .stButton>button { 
        background: linear-gradient(90deg, #00dbde 0%, #fc00ff 100%); 
        color: white; border-radius: 25px; font-weight: bold; border: none; height: 50px; width: 100%;
    }
    .result-card { border: 1px solid #30363d; border-radius: 15px; padding: 15px; background: #1c2128; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# API Setup
API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"
try:
    # Ye aapke Streamlit Secrets se token lega
    HF_TOKEN = st.secrets["HF_TOKEN"]
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
except:
    st.error("Error: Secrets mein HF_TOKEN nahi mila! Dashboard check karein.")
    st.stop()

# --- Helper: Background Removal via API ---
def remove_bg_api(image_bytes):
    try:
        response = requests.post(API_URL, headers=headers, data=image_bytes)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except:
        return None

# --- Main App ---
st.title("⚡ ChattyFroggy AI Turbo Studio")
st.write("Professional Background Removal & AI Enhancement")

upload = st.file_uploader("Apni Photo Upload karein", type=["jpg", "png", "jpeg"])

if upload:
    col_up, col_btn = st.columns([2, 1])
    with col_up:
        st.image(upload, caption="Original Photo", width=300)
    
    if st.button("Magic Turbo Remove ✨"):
        with st.spinner("AI Servers se connect ho raha hai..."):
            
            img_bytes = upload.getvalue()
            # Try Turbo Mode
            result_bytes = remove_bg_api(img_bytes)
            
            # If Turbo fails, use backup (rembg)
            if result_bytes is None:
                st.warning("Turbo API Busy hai, Backup Mode use ho raha hai...")
                from rembg import remove
                result_bytes = remove(img_bytes)
            
            if result_bytes:
                subject_img = Image.open(io.BytesIO(result_bytes)).convert("RGBA")
                
                # Auto-Enhance
                enhancer = ImageEnhance.Sharpness(subject_img)
                subject_img = enhancer.enhance(1.2)

                st.divider()
                st.subheader("Results")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.image(subject_img, caption="Transparent Result", use_container_width=True)
                
                with c2:
                    st.success("Process Complete!")
                    st.download_button(
                        label="📥 Download High Quality PNG",
                        data=result_bytes,
                        file_name="chattyfroggy_pro.png",
                        mime="image/png"
                    )

st.info("Tip: Agar 'Invalid Token' aaye, toh Streamlit Secrets mein HF_TOKEN format check karein.")