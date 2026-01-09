import streamlit as st
import pandas as pd
from datetime import datetime
import os
import urllib.parse
import re

# ======================
# CONFIG
# ======================
CLASS_REP_PHONE = "2349077352809"  # WhatsApp number (no +)
CSV_FILE = "attendance.csv"

st.set_page_config(page_title="Class Attendance", layout="centered")
st.title("📋 Class Attendance System")

# ======================
# CREATE CSV IF NOT EXISTS
# ======================
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Matric Number", "Name", "Course", "Arrival Time"])
    df.to_csv(CSV_FILE, index=False)

# ======================
# TIME VALIDATION
# ======================
def valid_time_format(time_text):
    return re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time_text)

# ======================
# STUDENT FORM
# ======================
st.subheader("Student Attendance")

with st.form("attendance_form"):
    matric = st.text_input("Matric Number")
    name = st.text_input("Full Name")
    course = st.text_input("Course Code")
    arrival_time = st.text_input(
        "Time Arrived (HH:MM)",
        placeholder="e.g. 08:15"
    )

    submit = st.form_submit_button("Submit Attendance")

if submit:
    if not (matric and name and course and arrival_time):
        st.error("❌ Please fill in all fields")

    elif not valid_time_format(arrival_time):
        st.error("❌ Invalid time format. Use HH:MM (24-hour format)")

    else:
        # Save attendance
        new_data = pd.DataFrame(
            [[matric, name, course, arrival_time]],
            columns=["Matric Number", "Name", "Course", "Arrival Time"]
        )
        new_data.to_csv(CSV_FILE, mode="a", header=False, index=False)

        # WhatsApp message
        message = f"""
New Attendance Submitted

Matric Number: {matric}
Name: {name}
Course: {course}
Arrival Time: {arrival_time}
"""

        encoded_message = urllib.parse.quote(message)
        whatsapp_link = f"https://wa.me/{CLASS_REP_PHONE}?text={encoded_message}"

        st.success("✅ Attendance submitted successfully")
        st.markdown(
            f"📲 **[Send Attendance to Class Rep on WhatsApp]( {whatsapp_link} )**",
            unsafe_allow_html=True
        )

