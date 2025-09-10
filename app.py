# -*- coding: utf-8 -*-
"""
Static Google Review QR Generator (No Files Saved)
- Generates QR code in-memory and displays it in the GUI.
- The QR code directly opens the Google review page (no hosting needed).
- Copies an AI-generated review suggestion to the clipboard.
"""

import qrcode
import random
import tkinter as tk
from tkinter import messagebox, scrolledtext, font
from PIL import Image, ImageTk

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

# ---------------- QR Generation Logic ----------------

def generate_qr():
    """
    Generates the QR code in memory, displays it, and copies the review.
    """
    try:
        # The final URL that directly opens the review dialog
        google_review_url = f"https://search.google.com/local/writereview?placeid={PLACE_ID}"

        # Generate QR code pointing directly to the review URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(google_review_url)
        qr.make(fit=True)

        # Create an image from the QR Code instance IN MEMORY
        img = qr.make_image(fill_color="black", back_color="white")

        # Display QR in the GUI without saving to a file
        # Convert the PIL image to a PhotoImage for Tkinter
        resized_img = img.resize((200, 200), Image.LANCZOS)
        qr_photo = ImageTk.PhotoImage(resized_img)
        
        qr_label.config(image=qr_photo)
        qr_label.image = qr_photo # Keep a reference to avoid garbage collection

        # Generate AI review and copy to clipboard
        ai_review = generate_ai_review()
        review_box.delete("1.0", tk.END)
        review_box.insert("1.0", ai_review)
        
        root.clipboard_clear()
        root.clipboard_append(ai_review)
        
        messagebox.showinfo("Success", "QR Code Generated!\n\nThe suggested review has been copied to your clipboard.")

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title(f"QR Generator - {BUSINESS_NAME}")
root.geometry("450x550")
root.resizable(False, False)
root.configure(bg="#f0f2f5")

main_frame = tk.Frame(root, padx=20, pady=20, bg="#f0f2f5")
main_frame.pack(fill="both", expand=True)

# --- Fonts ---
title_font = font.Font(family="Arial", size=14, weight="bold")
button_font = font.Font(family="Arial", size=12, weight="bold")
label_font = font.Font(family="Arial", size=11)

# --- Widgets ---
tk.Label(main_frame, text="Google Review QR Code", font=title_font, bg="#f0f2f5").pack(pady=(0, 15))

generate_button = tk.Button(
    main_frame, 
    text="Generate QR Code & Copy Review", 
    command=generate_qr, 
    font=button_font,
    bg="#007bff", 
    fg="white", 
    relief="flat", 
    padx=15, 
    pady=10, 
    cursor="hand2"
)
generate_button.pack(pady=10)

qr_label = tk.Label(main_frame, bg="#f0f2f5")
qr_label.pack(pady=15)

tk.Label(main_frame, text="AI Review Suggestion (Copied to Clipboard):", font=label_font, bg="#f0f2f5").pack(anchor="w")
review_box = scrolledtext.ScrolledText(
    main_frame, 
    width=50, 
    height=8, 
    wrap=tk.WORD, 
    font=("Arial", 10), 
    relief="solid", 
    borderwidth=1
)
review_box.pack(pady=5, fill="x", expand=True)

root.mainloop()  