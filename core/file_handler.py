import os
import base64
import zipfile
import tempfile
import streamlit as st

from io import BytesIO  
from PIL import Image
from pdf2image import convert_from_path

Image.MAX_IMAGE_PIXELS = None 

# File types
def is_image_file(filename: str) -> bool:
    return filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))

def is_pdf(filename: str) -> bool:
    return filename.lower().endswith((".pdf"))

def is_zip(filename: str) -> bool:
    return filename.lower().endswith((".zip"))

def process_image_file(filepath, file):  
    # Display image  
    img = Image.open(filepath)
    st.image(img, caption=file, use_container_width=True)  
  
    # Encode image as base64  
    with open(filepath, "rb") as image_file:  
        encoded = base64.b64encode(image_file.read()).decode('utf-8')  
    return [encoded]  # single-image list for consistency  
  
def process_pdf_file(filepath, file):  
    base64_images = []  
    try:  
        st.write(f"Extracting pages from **{file}**...")  
        pdf_images = convert_from_path(filepath)  
        for i, page in enumerate(pdf_images):  
            caption = f"{file} - Page {i+1}"  
            st.image(page, caption=caption, use_container_width=True)  
  
            # Save page image to buffer, then encode to base64  
            buffered = BytesIO()  
            page.save(buffered, format="PNG")  
            encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')  
            base64_images.append(encoded)  
    except Exception as e:  
        st.error(f"Failed to process {file}: {e}")  
    return base64_images  

# def process_pdf_file(filepath, file):
#     base64_images = []
#     try:
#         st.write(f"Extracting pages from **{file}**...")
#         # Open PDF file using PyMuPDF
#         pdf_document = fitz.open(filepath)
        
#         for page_num in range(pdf_document.page_count):
#             # Get the page
#             page = pdf_document[page_num]
#             caption = f"{file} - Page {page_num + 1}"
            
#             # Convert page to image
#             pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
#             img_bytes = pix.tobytes("png")
            
#             # Display image in Streamlit
#             st.image(img_bytes, caption=caption, use_container_width=True)
            
#             # Encode to base64
#             encoded = base64.b64encode(img_bytes).decode('utf-8')
#             base64_images.append(encoded)
            
#         pdf_document.close()
#         st.write(base64_images)
        
    # except Exception as e:
    #     st.error(f"Failed to process {file}: {e}")
    
    # return base64_images
  
def extract_zip_and_show(uploaded_file):  
    st.success("ZIP file uploaded!")  
    files_dict = {}  
  
    with tempfile.TemporaryDirectory() as tmpdir:  
        # Save uploaded zip to temp file  
        zip_path = os.path.join(tmpdir, "uploaded_file.zip")  
        with open(zip_path, "wb") as f:  
            f.write(uploaded_file.getbuffer())  
  
        # Extract ZIP  
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:  
            zip_ref.extractall(tmpdir)  
  
        st.info("Extracted files. Checking contents...")  
  
        for root, _, files in os.walk(tmpdir):  
            for file in files:  
                filepath = os.path.join(root, file)  
  
                if is_image_file(file):  
                    base64_images = process_image_file(filepath, file)  
                elif is_pdf(file):  
                    base64_images = process_pdf_file(filepath, file)  
                else:  
                    base64_images = []  
  
                if base64_images:  
                    files_dict[file] = base64_images  
  
        st.success(f"Done! {sum(len(v) for v in files_dict.values())} image(s) displayed.")  
        return files_dict 

def extract_from_image_or_pdf(uploaded_file, file_type):  
    if file_type == 'pdf':
        suffix = '.pdf'
    elif file_type == 'img':
        suffix = '.img'

    # Save uploaded_file to a temp file  
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tf:  
        tf.write(uploaded_file.getbuffer())  # Write bytes to temp file  
        temp_file_path = tf.name  
    # Get a suitable filename for display (if available)  
    try:  
        filename = uploaded_file.name  
    except AttributeError:  
        filename = os.path.basename(temp_file_path) 

    if file_type == 'pdf':
        base64_images = process_pdf_file(temp_file_path, filename)  
    elif file_type == 'img':
        base64_images = process_image_file(temp_file_path, filename)   
    
    
    files_dict = {} 
    if base64_images:  
        files_dict[filename] = base64_images
    
    st.success(f"Done! {sum(len(v) for v in files_dict.values())} image(s) displayed.")  
    
    return files_dict  

def handle_uploaded_file(uploaded_file):
    """
    Handles a single uploaded file.
    Returns a dict where key is filename and values are base64 codes of each image in each file.
    """
    filename = uploaded_file.name      

    if is_pdf(filename):
        results = extract_from_image_or_pdf(uploaded_file, file_type='pdf')
    elif is_image_file(filename):
        results = extract_from_image_or_pdf(uploaded_file, file_type='img')
    elif is_zip(filename):
        results = extract_zip_and_show(uploaded_file) 
    else:
        st.warning('Only pdf, png, jpg, jpeg, webp or a zipped file that only contains these file types can be uploaded')
    return results
