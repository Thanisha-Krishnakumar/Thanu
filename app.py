import streamlit as st
from roboflow import Roboflow
import numpy as np
from PIL import Image

# Secure API key
API_KEY = st.secrets["API_KEY"]

rf = Roboflow(api_key=API_KEY)
project = rf.workspace().project("forestfiredetection-kkcq0")
model = project.version(2).model

st.title("🌲🔥 Forest Fire Detection System")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, width=500)

    if st.button("Detect"):
        image_np = np.array(image)

        prediction = model.predict(image_np).json()

        fire_detected = False
        smoke_detected = False

        for pred in prediction["predictions"]:
            if pred["class"].lower() == "fire":
                fire_detected = True
            elif pred["class"].lower() == "smoke":
                smoke_detected = True

        if fire_detected:
            st.error("🔥 Fire Detected!")
        elif smoke_detected:
            st.warning("🌫 Smoke Detected!")
        else:
            st.success("✅ No Fire or Smoke Detected")
