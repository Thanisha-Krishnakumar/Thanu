import streamlit as st
from roboflow import Roboflow
import numpy as np
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Secure API key
API_KEY = st.secrets["API_KEY"]

rf = Roboflow(api_key=API_KEY)
project = rf.workspace().project("forestfiredetection-kkcq0")
model = project.version(2).model
def send_email_alert(alert_type):

    sender_email = st.secrets["SENDER_EMAIL"]
    sender_password = st.secrets["SENDER_PASSWORD"]
    receiver_email = st.secrets["OFFICER_EMAIL"]

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    location = "Anaimalai Forest Region, Tamil Nadu"
    latitude = "10.3610° N"
    longitude = "76.9661° E"
    zone = "Anaimalai Tiger Reserve – Zone 3"

    if alert_type == "fire":
    subject = "🚨 CRITICAL FIRE ALERT"
    body = f"""
    🚨 FOREST FIRE ALERT 🚨

   Fire Detected in Protected Forest Area!

      Location: {location}
      Zone: {zone}
      Latitude: {latitude}
      Longitude: {longitude}
      Detection Time: {current_time}


    elif alert_type == "smoke":
    subject = "SMOKE WARNING ALERT"
    body = f"""
    SMOKE WARNING ALERT

    Smoke Detected in Forest Area.

Location: {location}
Zone: {zone}
Latitude: {latitude}
Longitude: {longitude}
Detection Time: {current_time}

Possible early-stage wildfire.
Field verification recommended.
"""

    # Create email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Send email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()


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
            send_email_alert("fire")
            st.success("📧 Email Alert Sent to Forest Officer!")

        elif smoke_detected:
            st.warning("🌫 Smoke Detected!")
            send_email_alert("smoke")
            st.success("📧 Email Alert Sent to Forest Officer!")

        else:
            st.success("✅ No Fire or Smoke Detected")
