# -*- coding: utf-8 -*-
"""
Static Google Review QR Generator (Streamlit Web App Version)
- Generates a QR code and displays it on a web page.
- The QR code directly opens the Google review page.
- Generates an AI review suggestion for the user to copy.
- Automatically copies the review to clipboard (browser-based solution)
"""

import streamlit as st
import qrcode
import random
from PIL import Image
import io
import streamlit.components.v1 as components

# ---------------- Configuration ----------------
BUSINESS_NAME = "Ludhiana SEO Expert"
PLACE_ID = "ChIJP1UfWFWDGjkRxFYT32EgTVI"  # Your specific Google Place ID

# ---------------- Helper Functions ----------------

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

def copy_to_clipboard_js(text):
    """Generate JavaScript code to copy text to clipboard"""
    # Escape quotes and newlines in the text for JavaScript
    escaped_text = text.replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')
    
    js_code = f"""
    <script>
    function copyToClipboard() {{
        const text = '{escaped_text}';
        navigator.clipboard.writeText(text).then(function() {{
            // Show success message
            const msg = document.createElement('div');
            msg.innerHTML = '✅ Review copied to clipboard!';
            msg.style.cssText = 'position:fixed;top:20px;right:20px;background:#28a745;color:white;padding:10px;border-radius:5px;z-index:1000;';
            document.body.appendChild(msg);
            setTimeout(() => msg.remove(), 3000);
        }}).catch(function(err) {{
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            const msg = document.createElement('div');
            msg.innerHTML = '✅ Review copied to clipboard!';
            msg.style.cssText = 'position:fixed;top:20px;right:20px;background:#28a745;color:white;padding:10px;border-radius:5px;z-index:1000;';
            document.body.appendChild(msg);
            setTimeout(() => msg.remove(), 3000);
        }});
    }}
    
    // Automatically copy when this script loads
    copyToClipboard();
    </script>
    """
    return js_code

# ---------------- Streamlit Web App Interface ----------------

# Set the page title and layout
st.set_page_config(page_title="Review QR Generator", layout="centered")

# Display titles and information
st.title(f"Google Review QR Generator")
st.header(f"For: {BUSINESS_NAME}")
st.write("Click the button to generate a QR code that links directly to the Google review page. A sample review will also be generated and automatically copied to your clipboard.")

# Use Streamlit's session state to store the generated data
if 'qr_image' not in st.session_state:
    st.session_state.qr_image = None
if 'review_text' not in st.session_state:
    st.session_state.review_text = ""
if 'just_generated' not in st.session_state:
    st.session_state.just_generated = False

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
    st.session_state.just_generated = True

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
    
    # Create columns for the text area and copy button
    text_col, button_col = st.columns([4, 1])
    
    with text_col:
        st.text_area(
            label="Review text:", 
            value=st.session_state.review_text, 
            height=150,
            key="review_display"
        )
    
    with button_col:
        st.write("")  # Add some spacing
        st.write("")
        if st.button("📋 Copy", help="Copy review to clipboard"):
            # Trigger JavaScript to copy to clipboard
            components.html(copy_to_clipboard_js(st.session_state.review_text), height=0)
    
    # Auto-copy functionality - runs only when content is just generated
    if st.session_state.just_generated:
        st.info("📋 Review has been automatically copied to your clipboard!")
        # Execute JavaScript to copy to clipboard automatically
        components.html(copy_to_clipboard_js(st.session_state.review_text), height=0)
        # Reset the flag
        st.session_state.just_generated = False

# Add some styling and instructions
st.markdown("""
---
### Instructions:
1. Click the "Generate QR Code & Review" button
2. The review will be automatically copied to your clipboard
3. You can also manually copy using the "📋 Copy" button
4. Scan the QR code with your phone to open Google Reviews
5. Paste the review text when writing your review

**Note:** Clipboard functionality works best in modern browsers with HTTPS.
""")  
