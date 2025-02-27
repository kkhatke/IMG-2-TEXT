import streamlit as st
import pytesseract
import numpy as np
import cv2
from PIL import Image
from pdf2image import convert_from_bytes
import io
import pillow_heif
import os
import platform

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

# Function to set Tesseract path dynamically
def set_tesseract_path():
    if platform.system() == "Windows":
        # Windows path (adjust if needed)
        return r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    elif platform.system() == "Linux":
        # Default Linux path
        return "/usr/bin/tesseract"
    elif platform.system() == "Darwin":
        # macOS path (if using Mac)
        return "/opt/homebrew/bin/tesseract"
    else:
        raise EnvironmentError("Unsupported OS: Tesseract path must be set manually.")

# Set the Tesseract path
pytesseract.pytesseract.tesseract_cmd = set_tesseract_path()

# Print Tesseract version for debugging
print("Using Tesseract at:", pytesseract.pytesseract.tesseract_cmd)

# Title of the Streamlit app
st.title("📄 Image to Text Converter (OCR)")

# Instructions
st.write("Upload images (JPG, PNG, JPEG) to extract text.")

# File uploader
uploaded_files = st.file_uploader("Choose image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Function to preprocess image for better OCR results
def preprocess_image(image):
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    
    # Handle PNG with transparency by creating white background
    if len(img_array.shape) == 3 and img_array.shape[2] == 4:  # RGBA image
        # Create a white background
        background = np.ones_like(img_array, dtype=np.uint8) * 255
        # Only keep RGB channels for background
        background = background[:, :, :3]
        
        # Extract alpha channel
        alpha = img_array[:, :, 3] / 255.0
        
        # Expand alpha to 3 channels
        alpha = np.expand_dims(alpha, axis=-1)
        alpha = np.repeat(alpha, 3, axis=-1)
        
        # Blend foreground with white background
        img_array = alpha * img_array[:, :, :3] + (1 - alpha) * background
        img_array = img_array.astype(np.uint8)
    
    # Convert to grayscale if it's a color image
    if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Apply image enhancement
    # 1. Noise removal
    denoised = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # 2. Thresholding to improve contrast
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

# Function to extract text using Tesseract
def extract_text_from_image(image):
    try:
        # Preprocess the image
        processed_img = preprocess_image(image)
        
        # Use Tesseract config for better text extraction
        custom_config = r'--oem 3 --psm 6'
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(processed_img, config=custom_config)
        
        # Handle empty output
        if not text.strip():
            # Try with original image if processed image failed
            text = pytesseract.image_to_string(np.array(image), config=custom_config)
        
        return text
    except Exception as e:
        st.error(f"Error in OCR processing: {str(e)}")
        return f"Error: {str(e)}"

# Function to safely open image files of various formats
def safe_open_image(uploaded_file):
    # Read file bytes
    file_bytes = uploaded_file.read()
    
    # Create a BytesIO object
    image_bytes = io.BytesIO(file_bytes)
    
    try:
        # Try to open with PIL
        img = Image.open(image_bytes)
        
        # Convert to RGB mode to ensure compatibility
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGBA')
        elif img.mode != 'RGB':
            img = img.convert('RGB')
            
        return img
    except Exception as e:
        raise ValueError(f"Cannot open image file: {str(e)}")

# Processing Uploaded Files
if uploaded_files:
    extracted_texts = {}  # Dictionary to store extracted text
    
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        st.subheader(f"📂 Processing: {file_name}")
        
        try:
            # Check if the file is an image or PDF
            file_type = uploaded_file.type
            
            if file_type == "application/pdf":
                st.write("📜 Extracting text from PDF pages...")
                # Reset stream position
                uploaded_file.seek(0)
                images = convert_from_bytes(uploaded_file.read()) 
            else:
                # Reset stream position
                uploaded_file.seek(0)
                
                # Handle HEIC files specifically
                if file_name.lower().endswith('.heic'):
                    st.write("📸 Processing HEIC image...")
                
                # Safely open the image
                image = safe_open_image(uploaded_file)
                
                # Display the original image
                st.image(image, caption=f"Original Image: {file_name}", use_column_width=True)
                images = [image] 
            
            # Extract text from each image
            text_output = []
            for i, img in enumerate(images):
                with st.spinner(f"Extracting text from image {i+1}/{len(images)}..."):
                    extracted_text = extract_text_from_image(img)
                    text_output.append(extracted_text)
            
            extracted_texts[file_name] = "\n".join(text_output)
            
            # Display extracted text
            with st.expander(f"📄 Extracted Text from {file_name}", expanded=True):
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
        except Exception as e:
            st.error(f"Error processing {file_name}: {str(e)}")
    
# Footer
st.markdown("---")
st.markdown("🚀 Developed using **Streamlit** & **Tesseract OCR** | Supports Images")
