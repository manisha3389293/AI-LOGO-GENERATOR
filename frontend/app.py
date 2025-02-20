import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AI Logo Generator", layout="wide")

st.title("🎨 AI Logo Generator with Stable Diffusion")

col1, col2 = st.columns(2)

with col1:
    prompt = st.text_area("📝 Describe your logo:", "Minimalist modern tech logo")
    negative_prompt = st.text_area("🚫 What to avoid?", "Realistic, blurry, low resolution")
    width = st.slider("📏 Width", 256, 768, 256, step=128)
    height = st.slider("📐 Height", 256, 768, 256, step=128)

with col2:
    seed = st.number_input("🔢 Random Seed (Leave blank for random)", min_value=0, value=42, step=1)
    generate_button = st.button("🚀 Generate Logo")

st.markdown("---")

if generate_button:
    with st.spinner("Generating logo... Please wait ⏳"):
        response = requests.post("http://127.0.0.1:8000/generate_logo", json={
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "seed": seed if seed > 0 else None
        })

        if response.status_code == 200:
            image_data = response.json().get("image")
            if image_data:
                image_bytes = base64.b64decode(image_data)
                full_image = Image.open(BytesIO(image_bytes))

                # Create small preview
                preview_size = (256, 256)
                preview_image = full_image.copy()
                preview_image.thumbnail(preview_size)

                # Show preview in UI
                st.image(preview_image, caption="🖼️ Preview Logo (Resized)", use_container_width=False)

                # Full-size download
                img_buffer = BytesIO()
                full_image.save(img_buffer, format="PNG")
                st.download_button(label="📥 Download Full Logo", data=img_buffer.getvalue(),
                                   file_name="generated_logo.png", mime="image/png")
            else:
                st.error("⚠️ Failed to generate image.")
        else:
            st.error("⚠️ API request failed. Try again.")

st.markdown("⚡ **Made with love by Manisha**")
