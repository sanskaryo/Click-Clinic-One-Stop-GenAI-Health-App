from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import pdfplumber

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Page Config ---
st.set_page_config(
    page_title="Click Clinic - Medical Document Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function definitions (keeping existing functions)
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    inputs = []
    if input_text:
        inputs.append(input_text)
    if image:
        inputs.append(image[0])
    if prompt:
        inputs.append(prompt)
    if not inputs:
        raise ValueError("No valid input provided for the AI model.")
    response = model.generate_content(inputs)
    return response.text if response and hasattr(response, 'text') else None

def extract_pdf_text(pdf_file):
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        raise RuntimeError(f"Error extracting text from PDF: {e}")

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded or captured")

def print_praise():
        praise_quotes = """
        Team Code Khildai

    2nd Year Students,
    B.Tech CSE (AIML & IOT)
    GLA UNIVERSITY
        """
        title = "**Developed By -**\n\n"
        return title + praise_quotes

# Custom CSS styling
st.markdown("""
    <style>
    .title {
        text-align: left;
        font-size: 35px;
        font-weight: bold;
        color: black;
    }
    .result-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #3498db;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px dashed #3498db;
    }
    .analyze-button {
        background-color: #3498db !important;
        color: white !important;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        transition: background-color 0.3s;
        width: 100%;
        margin: 10px 0;
    }
    .analyze-button:hover {
        background-color: #2980b9 !important;
    }
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    .success-message {
        padding: 10px;
        background-color: #d4edda;
        border-radius: 5px;
        color: #155724;
        margin: 10px 0;
    }
    .error-message {
        padding: 10px;
        background-color: #f8d7da;
        border-radius: 5px;
        color: #721c24;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image('logo_transparent.png', caption='ClickClinic : Your Health, Just a Click Away 🏥')
    
    # Features in an expander
    with st.expander("🚀 Features", expanded=False):
        st.markdown("- Upload or Capture Medical Documents")
        st.markdown("- Instant Analysis of Prescriptions")
        st.markdown("- Lab Report Interpretation")
        st.markdown("- PDF Text Extraction")
    
    st.write("---")
    st.success(print_praise())
    st.write("---")
    
    st.markdown(
        "<3 style='text-align: center;'>Developed with ❤️ for AI by <a style='text-decoration: none' href='https://www.linkedin.com/in/sanskar-khandelwal-611249210/'>Team code E Khiladi </a></3>",
        unsafe_allow_html=True
    )
    
    # # Visitors Count
    # st.markdown('''
    #     <center>
    #     <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40"  border="0" /></h1>
    #     </center>
    # ''', unsafe_allow_html=True)

# Main Content
st.title("🏥 Click Clinic - Medical Document Analyzer")
st.markdown("##### Instantly Analyze Prescriptions and Lab Reports with AI")
st.markdown("---")

# File Upload Section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

image = None
image_source = None

with col1:
    uploaded_file = st.file_uploader(
        "📤 Upload Medical Document:",
        type=["jpg", "jpeg", "png", "pdf"],
        help="Upload prescriptions, lab reports, or medical documents"
    )
    if uploaded_file:
        image = uploaded_file
        image_source = "upload"

with col2:
    enable_camera = st.checkbox("📸 Enable Camera Capture")
    picture = st.camera_input("Capture Document:", disabled=not enable_camera)
    if picture:
        image = picture
        image_source = "camera"

st.markdown('</div>', unsafe_allow_html=True)

# Display uploaded or captured image
if image:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    if image_source == "upload" and uploaded_file.type == "application/pdf":
        try:
            pdf_text = extract_pdf_text(image)
            st.markdown("### 📄 Extracted PDF Text")
            st.text_area("", pdf_text, height=300)
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
    else:
        try:
            displayed_image = Image.open(image)
            st.image(
                displayed_image,
                caption=f"Selected Document ({'Camera' if image_source == 'camera' else 'Upload'})",
                use_column_width=True
            )
            st.success(f"Document loaded successfully! 🎉")
        except Exception as e:
            st.error(f"Error displaying image: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis Section
if st.button("🔍 Analyze Document", key="analyze_button", use_container_width=True):
    if image:
        try:
            with st.spinner("Analyzing document... Please wait"):
                input_text = ""
                image_data = None

                if image_source == "upload" and uploaded_file.type == "application/pdf":
                    input_text = extract_pdf_text(image)
                    if not input_text.strip():
                        st.warning("⚠️ The PDF appears to be empty or contains no readable text.")
                        st.stop()
                else:
                    image_data = input_image_setup(image)

                if not input_text and not image_data:
                    st.warning("⚠️ No valid data found in the uploaded document.")
                    st.stop()

                input_prompt = """
                You are an AI healthcare assistant. Analyze the uploaded medical document (image or PDF) and provide the following insights in a structured, easy-to-read format:
                
                **1. Prescription Details:**
                - Doctor's Name and Specialization (if mentioned)
                - Patient's Name, Age, and Gender
                - Medications with their Dosages and Purposes
                
                **2. Lab Report Analysis:**
                - Test Names and Results
                - Interpretation of results (e.g., normal/abnormal, medical implications)
                
                **3. Notes and Recommendations:**
                - Diagnosis or Observations (if mentioned)
                - Follow-up Instructions (if any)
                
                Please ensure the response is clear, concise, and professionally formatted.
                """

                response = get_gemini_response(input_text, image_data, input_prompt)

                if response:
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.subheader("📋 Analysis Results")
                    st.markdown(response)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No response received from the AI model. Please try again.")
        except Exception as e:
            st.error(f"Error analyzing the document: {e}")
    else:
        st.warning("⚠️ Please upload or capture a document to analyze.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>© 2024 Click Clinic - Medical Document Analyzer. All rights reserved.</p>",
    unsafe_allow_html=True
)