# -*- coding: utf-8 -*-
"""
Static Google Review QR Generator (Streamlit Web App Version)
- Generates a QR code and displays it on a web page.
- The QR code directly opens the Google review page.
- Generates an AI review suggestion for the user to copy.
"""

import streamlit as st
import qrcode
import random
from PIL import Image
import io  # Needed to handle image data in memory

# ---------------- Configuration ----------------
BUSINESS_NAME = "Ludhiana SEO Expert"
PLACE_ID = "ChIJP1UfWFWDGjkRxFYT32EgTVI"  # Your specific Google Place ID

# ---------------- Helper Functions (This part is unchanged) ----------------

def generate_ai_review():
    """Generate a random positive review for the business."""
    openings = [
        "Absolutely wonderful experience with", "Had a fantastic time working with",
        "Truly impressed with the service from", "A big thank you to the team at",
        "Couldn't be happier with the results from", "Five stars all the way for",
        "An amazing company! I loved my experience with", "Exceptional service and expertise from"
    ]
    qualities = [
        "the team was incredibly professional and knowledgeable,", "they were super helpful and responsive,",
        "the customer service was top-notch,",
        "the quality of their work is outstanding,", "their attention to detail is second to none,"
    ]
    actions = [
        "making the whole process smooth and easy.", "and they went above and beyond for me.",
        "which made my day so much better.", "and I felt truly valued as a customer.",
        "and the results exceeded all my expectations.", "creating a genuinely positive and great atmosphere."
    ]
    recommendations = [
        "I will definitely be back for future projects!", "Would highly recommend them to everyone!",
        "Can't wait to work with them again!", "This is my new go-to expert!",
        "You have earned a loyal customer!", "Keep up the fantastic work!"
    ]

    review = (f"{random.choice(openings)} {BUSINESS_NAME}! {random.choice(qualities)} "
              f"{random.choice(actions)} {random.choice(recommendations)}")
    return review

# ---------------- Streamlit Web App Interface (This part is completely new) ----------------

# Set the page title and layout
st.set_page_config(page_title="Review QR Generator", layout="centered")

# Display titles and information
st.title(f"Google Review QR Generator")
st.header(f"For: {BUSINESS_NAME}")
st.write("Click the button to generate a QR code that links directly to the Google review page. A sample review will also be generated for inspiration.")

# Use Streamlit's session state to store the generated data
# This prevents the QR code from disappearing after it's generated
if 'qr_image' not in st.session_state:
    st.session_state.qr_image = None
if 'review_text' not in st.session_state:
    st.session_state.review_text = ""

# Create the main button
if st.button("🚀 Generate QR Code & Review", type="primary"):
    # This block of code runs ONLY when the button is clicked

    # --- QR Generation Logic ---
    google_review_url = f"https://search.google.com/local/writereview?placeid={PLACE_ID}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(google_review_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a memory buffer instead of a file
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Store the generated data in the session state
    st.session_state.qr_image = byte_im
    st.session_state.review_text = generate_ai_review()

# --- Display the results if they exist in the session state ---
if st.session_state.qr_image:
    st.divider()
    
    # Use columns for a nice layout
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(st.session_state.qr_image, width=200)
    with col2:
        st.success("QR Code Generated!")
        st.caption("Scan this with your phone to go directly to the review page.")
    
    st.subheader("AI-Generated Review Suggestion:")
    st.text_area(
        label="You can copy this text:", 
        value=st.session_state.review_text, 
        height=150
    )     
