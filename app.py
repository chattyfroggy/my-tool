import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance
import io
import requests
import urllib.parse

# Page Setup
st.set_page_config(page_title="AI Photo Studio Max", layout="wide")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background: linear-gradient(45deg, #00dbde 0%, #fc00ff 100%); color: white; border: none; font-weight: bold; width: 100%; height: 50px; border-radius: 12px; }
    .main-card { background: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 AI Photo Studio Max")
st.write("Background hatayein aur AI se naya background likh kar banayein!")

# --- Main Interface ---
upload = st.file_uploader("Step 1: Apni Photo Upload karein", type=["jpg", "png", "jpeg"])

if upload:
    # Saamne dikhne wale options
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Step 2: Background Style Chunein")
    
    col_mode, col_extra = st.columns([1, 2])
    
    with col_mode:
        mode = st.selectbox("Style:", ["AI Magic Generate", "Solid Color", "Transparent"])
    
    ai_prompt = ""
    bg_color = "#ffffff"
    
    with col_extra:
        if mode == "AI Magic Generate":
            # Yahan hai aapka prompt box jo ab saamne dikhega
            ai_prompt = st.text_input("Kya background banana hai? (English mein likhein)", "Modern luxury office, 8k, cinematic lighting")
        elif mode == "Solid Color":
            bg_color = st.color_picker("Color Chunein", "#007BFF")
    st.markdown('</div>', unsafe_allow_html=True)

    # Processing Button
    if st.button("Magic Edit Shuru Karein ✨"):
        with st.spinner("AI Magic kaam kar raha hai..."):
            # 1. Background Removal
            img_bytes = upload.getvalue()
            subject_bytes = remove(img_bytes)
            subject = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")

            # 2. Background Creation
            if mode == "AI Magic Generate":
                encoded_prompt = urllib.parse.quote(ai_prompt)
                gen_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={subject.width}&height={subject.height}&nologo=true"
                response = requests.get(gen_url)
                bg_img = Image.open(io.BytesIO(response.content)).convert("RGBA")
                bg_img = bg_img.resize(subject.size, Image.Resampling.LANCZOS)
                final_img = Image.alpha_composite(bg_img, subject)
            elif mode == "Solid Color":
                h = bg_color.lstrip('#')
                rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                new_bg = Image.new("RGBA", subject.size, rgb + (255,))
                final_img = Image.alpha_composite(new_bg, subject)
            else:
                final_img = subject

            # Results Display
            c1, c2 = st.columns(2)
            with c1: st.image(upload, caption="Original", use_container_width=True)
            with c2: st.image(final_img, caption="AI Result", use_container_width=True)

            # Download
            buf = io.BytesIO()
            final_img.convert("RGB").save(buf, format="JPEG")
            st.download_button("📥 Download Result", buf.getvalue(), "ai_result.jpg", "image/jpeg")
