import streamlit as st
from rembg import remove
from PIL import Image
import io
import gc # Garbage collector memory saaf rakhne ke liye

st.set_page_config(page_title="ChattyFroggy BG Remover", layout="centered")

# Custom CSS for better look
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("✂️ Simple Background Remover")
st.write("Upload a photo and wait for the magic!")

upload = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if upload:
    input_image = Image.open(upload)
    st.image(input_image, caption="Original Image", use_container_width=True)
    
    if st.button("Clean Background Now"):
        with st.spinner("AI Model Loading... (Pehli baar mein 2-3 min lagenge, please wait)"):
            try:
                # Memory saaf karna
                gc.collect()
                
                # Processing
                img_bytes = upload.getvalue()
                output_bytes = remove(img_bytes)
                
                # Result display
                result_img = Image.open(io.BytesIO(output_bytes))
                st.image(result_img, caption="Result", use_container_width=True)
                
                st.download_button(
                    label="Download Transparent Image",
                    data=output_bytes,
                    file_name="cleared_image.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Server is busy: {e}. Please refresh and try again.")
