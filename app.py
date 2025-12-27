import streamlit as st
from rembg import remove
from PIL import Image, ImageDraw
import io
import requests
import urllib.parse

st.set_page_config(page_title="AI Photo Studio Max", layout="wide")

# Modern CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background: linear-gradient(45deg, #00C9FF 0%, #92FE9D 100%); color: #000; border: none; font-weight: bold; width: 100%; height: 50px; border-radius: 12px; }
    .result-card { border: 1px solid #30363d; border-radius: 15px; padding: 15px; background: #1c2128; margin-bottom: 25px; text-align: center; }
    .download-btn { margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 AI Pro Studio (Photoroom Edition)")
st.write("Solid colors purane ho gaye! Ab use karein **Smart Gradients aur Studio Textures**.")

# --- Step 1: Upload ---
upload = st.file_uploader("Apni Photo yahan upload karein", type=["jpg", "png", "jpeg"])

if upload:
    # Sidebar for custom tweaks
    st.sidebar.header("Custom Settings")
    custom_idea = st.sidebar.text_input("AI Style Idea:", "Luxury aesthetic, blurred lights")
    
    if st.button("Magic Studio Shuru Karein ✨"):
        with st.spinner("AI 4 Professional Designs bana raha hai..."):
            # Background Removal
            img_bytes = upload.getvalue()
            subject_bytes = remove(img_bytes)
            subject = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
            w, h = subject.size

            results = []

            # --- VARIANT 1: Modern Mesh Gradient (Soft Blue/Purple) ---
            try:
                grad_url = f"https://image.pollinations.ai/prompt/soft%20mesh%20gradient%20blue%20and%20purple%20aesthetic?width={w}&height={h}&nologo=true&seed=12"
                bg1 = Image.open(io.BytesIO(requests.get(grad_url).content)).convert("RGBA").resize((w, h))
                results.append({"img": Image.alpha_composite(bg1, subject), "label": "Modern Gradient"})
            except: pass

            # --- VARIANT 2: Studio Texture (Grey Concrete/Paper) ---
            try:
                text_url = f"https://image.pollinations.ai/prompt/grey%20studio%20wall%20texture%20professional%20photography?width={w}&height={h}&nologo=true&seed=88"
                bg2 = Image.open(io.BytesIO(requests.get(text_url).content)).convert("RGBA").resize((w, h))
                results.append({"img": Image.alpha_composite(bg2, subject), "label": "Studio Texture"})
            except: pass

            # --- VARIANT 3: Smart AI Background (From User Input) ---
            try:
                encoded_p = urllib.parse.quote(custom_idea)
                ai_url = f"https://image.pollinations.ai/prompt/{encoded_p}?width={w}&height={h}&nologo=true&seed=45"
                bg3 = Image.open(io.BytesIO(requests.get(ai_url).content)).convert("RGBA").resize((w, h))
                results.append({"img": Image.alpha_composite(bg3, subject), "label": "AI Custom Style"})
            except: pass

            # --- VARIANT 4: Clean Shadow White (Passport/E-commerce) ---
            bg4 = Image.new("RGBA", (w, h), (255, 255, 255, 255))
            results.append({"img": Image.alpha_composite(bg4, subject), "label": "Minimalist White"})

            # --- DISPLAY GRID (2x2) ---
            st.subheader("Aapke Pro Results:")
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            grid_cols = [col1, col2, col3, col4]

            for i, res in enumerate(results):
                with grid_cols[i]:
                    st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
                    st.image(res["img"], caption=res["label"], use_container_width=True)
                    
                    # Download
                    buf = io.BytesIO()
                    res["img"].convert("RGB").save(buf, format="JPEG")
                    st.download_button(f"📥 Save {res['label']}", buf.getvalue(), f"studio_{i}.jpg", "image/jpeg", key=f"dl_{i}")
                    st.markdown('</div>', unsafe_allow_html=True)
