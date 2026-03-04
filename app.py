from twilio.rest import Client
import streamlit as st
from roboflow import Roboflow
import numpy as np
from PIL import Image

# Secure API key
API_KEY = st.secrets["API_KEY"]

rf = Roboflow(api_key=API_KEY)
project = rf.workspace().project("forestfiredetection-kkcq0")
model = project.version(2).model
def send_sms_alert(alert_type):
    client = Client(
        st.secrets["TWILIO_SID"],
        st.secrets["TWILIO_AUTH"]
    )

    if alert_type == "fire":
        message_body = "🚨 CRITICAL ALERT: Forest Fire Detected! Immediate action required."
    elif alert_type == "smoke":
        message_body = "⚠ WARNING: Smoke Detected in Forest Area. Possible early fire stage."

    client.messages.create(
        body=message_body,
        from_=st.secrets["TWILIO_PHONE"],
        to=st.secrets["ALERT_PHONE"]
    )

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
    st.write("🔥 Fire Detected!")
    send_sms_alert("fire")
    st.success("🚨 Fire Alert Sent Successfully!")

elif smoke_detected:
    st.write("🌫 Smoke Detected!")
    send_sms_alert("smoke")
    st.success("⚠ Smoke Alert Sent Successfully!")

else:
    st.write("✅ No Fire or Smoke Detected")
