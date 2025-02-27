import streamlit as st
import pytesseract
import numpy as np
import cv2
from PIL import Image
from pdf2image import convert_from_bytes
import io

# Set Tesseract OCR Path (Windows users)
# Uncomment and modify the path if necessary
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Title of the Streamlit app
st.title("📄 Image to Text Converter (OCR)")

# Instructions
st.write("Upload images (JPG, PNG, TIFF, WebP, HEIC) to extract text.")

# File uploader
uploaded_files = st.file_uploader("Choose image files", type=["jpg", "jpeg", "png", "tiff", "webp", "heic"], accept_multiple_files=True)

# Function to extract text using Tesseract
def extract_text_from_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    return pytesseract.image_to_string(gray)

# Processing Uploaded Files
if uploaded_files:
    extracted_texts = {}  # Dictionary to store extracted text

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        st.subheader(f"📂 Processing: {file_name}")

        # Check if the file is an image or PDF
        if uploaded_file.type == "application/pdf":
            st.write("📜 Extracting text from PDF pages...")
            images = convert_from_bytes(uploaded_file.read())  # Convert PDF to images
        else:
            image = Image.open(uploaded_file)
            images = [image]  # Treat single image as a list

        # Extract text from each image
        text_output = []
        for img in images:
            extracted_text = extract_text_from_image(img)
            text_output.append(extracted_text)

        extracted_texts[file_name] = "\n".join(text_output)

        # Display extracted text
        with st.expander(f"📄 Extracted Text from {file_name}"):
            st.text_area("", extracted_texts[file_name], height=200)

        # Provide a download button for the extracted text
        text_file = io.BytesIO()
        text_file.write(extracted_texts[file_name].encode())
        text_file.seek(0)
        st.download_button(
            label="📥 Download Extracted Text",
            data=text_file,
            file_name=f"{file_name}.txt",
            mime="text/plain"
        )

# Footer
st.markdown("---")
st.markdown("🚀 Developed using **Streamlit** & **Tesseract OCR** | Supports Images")
