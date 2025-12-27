import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance
import io
import requests
import urllib.parse

st.set_page_config(page_title="AI Photo Studio Ultimate", layout="wide")

# Modern Dark UI CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background: linear-gradient(45deg, #00F260 0%, #0575E6 100%); color: white; border: none; font-weight: bold; width: 100%; height: 50px; border-radius: 12px; }
    .result-card { border: 1px solid #30363d; border-radius: 15px; padding: 15px; background: #1c2128; margin-bottom: 25px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 AI Photo Studio Ultimate")
st.write("Enhance, Remove Background, aur ab **Sahi Size** mein download karein!")

# --- Helper Function: Fit Subject into Target Size ---
def fit_subject_to_canvas(subject_img, target_w, target_h):
    # 1. Create a transparent canvas of target size
    canvas = Image.new("RGBA", (target_w, target_h), (0,0,0,0))
    
    # 2. Resize subject to fit well within the canvas (maintaining aspect ratio)
    # We use a slightly smaller factor (0.9) so it doesn't touch the edges
    max_w = int(target_w * 0.95)
    max_h = int(target_h * 0.95)
    subject_img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    
    # 3. Center the subject onto the canvas
    offset_x = (target_w - subject_img.width) // 2
    offset_y = (target_h - subject_img.height) // 2
    canvas.paste(subject_img, (offset_x, offset_y), subject_img)
    return canvas

# --- Step 1: Upload & Settings ---
col_up, col_set = st.columns([1.5, 1])

with col_up:
    upload = st.file_uploader("Apni Photo yahan upload karein", type=["jpg", "png", "jpeg"])

with col_set:
    st.subheader("🛠️ Pro Settings")
    do_enhance = st.checkbox("Auto-Enhance Quality ✨", value=True)
    
    # --- NEW: Size Selection ---
    SIZE_MAP = {
        "Original Size": None,
        "Passport (3.5x4.5cm)": (827, 1063), # High Res for Print
        "Square (1:1 Instagram)": (1080, 1080),
        "Portrait (4:5 Social)": (1080, 1350),
        "Landscape (16:9 YouTube)": (1920, 1080)
    }
    selected_size_name = st.selectbox("Output Size / Format:", list(SIZE_MAP.keys()))
    target_dims = SIZE_MAP[selected_size_name]

    custom_idea = st.text_input("AI Style Idea (Optional):", "Modern blurred office")

if upload:
    if st.button("Generate All Versions ✨"):
        with st.spinner("AI processing, resizing aur enhancement chal rahi hai..."):
            
            # 1. Background Removal
            img_bytes = upload.getvalue()
            subject_bytes = remove(img_bytes)
            subject_raw = Image.open(io.BytesIO(subject_bytes)).convert("RGBA")
            
            # 2. Image Enhancement
            if do_enhance:
                enhancer = ImageEnhance.Sharpness(subject_raw)
                subject_raw = enhancer.enhance(1.4)
                enhancer = ImageEnhance.Contrast(subject_raw)
                subject_raw = enhancer.enhance(1.1)
                enhancer = ImageEnhance.Color(subject_raw)
                subject_raw = enhancer.enhance(1.1)

            # 3. Determine Final Dimensions & Subject Placement
            if target_dims is None:
                w, h = subject_raw.size
                final_subject_layer = subject_raw
            else:
                w, h = target_dims
                # Naya function call jo subject ko naye size mein fit karega
                final_subject_layer = fit_subject_to_canvas(subject_raw, w, h)

            results = []

            # --- VARIANT 1: Transparent PNG (Resized) ---
            results.append({"img": final_subject_layer, "label": f"Transparent ({selected_size_name})", "format": "PNG"})

            # --- VARIANT 2: Modern Gradient (Generated at target size) ---
            try:
                grad_url = f"https://image.pollinations.ai/prompt/soft%20mesh%20gradient%20blue%20purple%20peach%20aesthetic?width={w}&height={h}&nologo=true"
                bg1 = Image.open(io.BytesIO(requests.get(grad_url).content)).convert("RGBA").resize((w, h))
                results.append({"img": Image.alpha_composite(bg1, final_subject_layer), "label": "Modern Gradient", "format": "JPEG"})
            except: pass

            # --- VARIANT 3: Professional Studio White (Passport standard) ---
            bg2 = Image.new("RGBA", (w, h), (255, 255, 255, 255))
            results.append({"img": Image.alpha_composite(bg2, final_subject_layer), "label": "Studio White (Official)", "format": "JPEG"})

            # --- VARIANT 4: AI Custom Style (Generated at target size) ---
            try:
                encoded_p = urllib.parse.quote(custom_idea)
                ai_url = f"https://image.pollinations.ai/prompt/{encoded_p}?width={w}&height={h}&nologo=true"
                bg3 = Image.open(io.BytesIO(requests.get(ai_url).content)).convert("RGBA").resize((w, h))
                results.append({"img": Image.alpha_composite(bg3, final_subject_layer), "label": "AI Custom Style", "format": "JPEG"})
            except: pass

            # --- DISPLAY GRID ---
            st.divider()
            st.subheader(f"Results: {selected_size_name} Format")
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            grid_cols = [col1, col2, col3, col4]

            for i, res in enumerate(results):
                with grid_cols[i]:
                    st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
                    st.image(res["img"], caption=res["label"], use_container_width=True)
                    
                    # Download Logic
                    buf = io.BytesIO()
                    if res["format"] == "PNG":
                        res["img"].save(buf, format="PNG")
                        ext = "png"
                        mime = "image/png"
                    else:
                        res["img"].convert("RGB").save(buf, format="JPEG")
                        ext = "jpg"
                        mime = "image/jpeg"
                    
                    st.download_button(f"📥 Download", buf.getvalue(), f"result_{i}_{selected_size_name}.{ext}", mime, key=f"dl_{i}")
                    st.markdown('</div>', unsafe_allow_html=True)
