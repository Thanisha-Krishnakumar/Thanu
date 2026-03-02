import streamlit as st
from inference import get_model
import numpy as np
from PIL import Image

API_KEY = "dvgsVyqzN3xfG3PwwtuE"

model = get_model(
    model_id="forestfiredetection-kkcq0/2",
    api_key=API_KEY
)

st.title("🌲🔥 Forest Fire Detection System")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, width=500)

    if st.button("Detect"):
        image_np = np.array(image)
        result = model.infer(image_np)[0]
        predictions = result.predictions

        fire_detected = False
        smoke_detected = False

        for pred in predictions:
            if pred.class_name.lower() == "fire":
                fire_detected = True
            elif pred.class_name.lower() == "smoke":
                smoke_detected = True

        if fire_detected:
            st.error("🔥 Fire Detected!")
        elif smoke_detected:
            st.warning("🌫 Smoke Detected!")
        else:
            st.success("✅ No Fire or Smoke Detected")
