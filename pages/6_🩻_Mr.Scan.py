import streamlit as st
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import pytesseract
from PIL import Image
import pdfplumber
from io import BytesIO
import requests
from groq import Groq
import dotenv
import os

# --- Page Config ---
st.set_page_config(
    page_title="Medical Image Diagnosis",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize environment variables and Groq client
dotenv.load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq()

# Model paths and loading
chest_xray_model_path = 'Mr.Scan\Chest-X_Ray_inc.h5'
mri_model_path = 'Mr.Scan\Brain.h5'
bone_model_path = 'Mr.Scan\Bone_fracture_optimized.h5'
labels = ['glioma_tumor', 'no_tumor', 'meningioma_tumor', 'pituitary_tumor']

# Load models with error handling
try:
    chest_xray_model = load_model(chest_xray_model_path)
    mri_model = load_model(mri_model_path)
    bone_model = load_model(bone_model_path)
except Exception as e:
    st.error(f"Error loading models: {str(e)}")

# Function to preprocess images
def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocess the uploaded image for model prediction
    """
    try:
        img = Image.open(image).convert('RGB')
        img = img.resize(target_size)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        return img_array
    except Exception as e:
        st.error(f"Error preprocessing image: {str(e)}")
        return None

# Prediction functions
def predict_xray(img_array):
    """
    Predict pneumonia from chest X-ray
    """
    try:
        prediction = chest_xray_model.predict(img_array)
        confidence = prediction[0][0] * 100
        result = 'Positive for Pneumonia' if prediction[0] > 0.5 else 'Negative for Pneumonia'
        return f"{result} (Confidence: {confidence:.2f}%)"
    except Exception as e:
        return f"Error in X-ray prediction: {str(e)}"

def predict_mri(img_array):
    """
    Predict brain tumor type from MRI
    """
    try:
        prediction = mri_model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)
        confidence = np.max(prediction) * 100
        return f"{labels[predicted_class[0]]} (Confidence: {confidence:.2f}%)"
    except Exception as e:
        return f"Error in MRI prediction: {str(e)}"

def predict_bone(img_array):
    """
    Predict bone fracture from scan
    """
    try:
        prediction = bone_model.predict(img_array)
        confidence = prediction[0][0] * 100
        result = 'Fracture Detected' if prediction[0] > 0.01 else 'No Fracture Detected'
        return f"{result} (Confidence: {confidence:.2f}%)"
    except Exception as e:
        return f"Error in bone scan prediction: {str(e)}"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    """
    Extract text content from uploaded PDF file
    """
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return ""

# Function to call Groq's Llama model
def llama_vision_detect(scan_result, report_text, feelings, location):
    """
    Analyze medical data using Groq's Llama model
    """
    try:
        prompt = f"""
        As a medical AI assistant, please analyze the following information and provide a comprehensive assessment:

        Scan Analysis Result: {scan_result}
        Medical Report Content: {report_text}
        Patient Symptoms: {feelings}
        Patient Location: {location}

        Please provide:
        1. A summary of the findings
        2. Potential implications
        3. Recommended next steps
        4. Any relevant location-based healthcare suggestions
        """
        
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in AI analysis: {str(e)}"

# Custom CSS
st.markdown("""
    <style>
    .title {
        text-align: left;
        font-size: 35px;
        font-weight: bold;
        color: black;
        margin-bottom: 20px;
    }
    .diagnosis-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3498db;
        transition: all 0.3s ease;
    }
    .diagnosis-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }
    .upload-section {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border: 2px dashed #3498db;
    }
    .result-section {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #2ecc71;
    }
    .warning-section {
        background-color: #fff3cd;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #ffc107;
    }
    .error-section {
        background-color: #f8d7da;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #dc3545;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 2px solid #3498db;
    }
    .stSelectbox>div>div>select {
        border-radius: 5px;
        border: 2px solid #3498db;
    }
    .confidence-high {
        color: #2ecc71;
        font-weight: bold;
    }
    .confidence-medium {
        color: #f1c40f;
        font-weight: bold;
    }
    .confidence-low {
        color: #e74c3c;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def print_praise():
        praise_quotes = """
        Team Manthan

    2nd Year Students,
    B.Tech(Hons) CSE
    GLA UNIVERSITY
        """
        title = "**Developed By -**\n\n"
        return title + praise_quotes


# Sidebar
with st.sidebar:
    st.image('logo_transparent.png', caption='Medical Image Diagnosis System 🩺')
    
    with st.expander("ℹ️ About", expanded=True):
        st.write("""
        This advanced medical diagnostic system utilizes state-of-the-art AI models to analyze:
        - Chest X-rays for Pneumonia Detection
        - Brain MRI for Tumor Classification
        - Bone Scans for Fracture Detection
        """)
    
    with st.expander("🚀 Features", expanded=False):
        st.markdown("""
        - Multi-modal scan analysis
        - PDF report text extraction
        - AI-powered recommendations
        - Location-based insights
        - Confidence scoring
        """)
    
    with st.expander("📋 Instructions", expanded=False):
        st.markdown("""
        1. Select scan type
        2. Upload medical image
        3. Upload report (optional)
        4. Describe symptoms
        5. Enter location
        6. Click analyze for results
        """)
    
    st.write("---")
    st.success(print_praise())

# Main content
st.markdown('<div class="title">🩺 Medical Image Diagnosis System</div>', unsafe_allow_html=True)
st.markdown("##### Radhe Radhe 🙏 Welcome to the Advanced Medical Diagnostic Tool")

# Create columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    scan_type = st.selectbox(
        "Select the type of scan",
        options=["Select Scan Type", "X-ray", "MRI", "Bone Scan"]
    )
    
    uploaded_image = st.file_uploader("Upload a medical scan image (JPG, PNG, JPEG)", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Scan")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="diagnosis-card">', unsafe_allow_html=True)
    st.subheader("📊 Quick Diagnosis")
    if uploaded_image and scan_type != "Select Scan Type":
        img_array = preprocess_image(uploaded_image)
        
        if img_array is not None:
            with st.spinner('Analyzing image...'):
                if scan_type == "X-ray":
                    scan_result = predict_xray(img_array)
                elif scan_type == "MRI":
                    scan_result = predict_mri(img_array)
                elif scan_type == "Bone Scan":
                    scan_result = predict_bone(img_array)
                
                st.markdown(f"**Result:** {scan_result}")
    else:
        st.info("Please upload an image and select scan type for diagnosis")
    st.markdown('</div>', unsafe_allow_html=True)

# Report Analysis Section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.subheader("📄 Report Analysis")
uploaded_pdf = st.file_uploader("Upload a medical report (PDF)", type=["pdf"])

if uploaded_pdf:
    col3, col4 = st.columns([1, 1])
    with col3:
        with st.spinner('Extracting text from the report...'):
            report_text = extract_text_from_pdf(uploaded_pdf)
        st.text_area("Extracted Report", report_text, height=200)
    
    with col4:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        feelings = st.text_area("Describe your symptoms:", height=100)
        location = st.text_input("Your location:")
        st.markdown('</div>', unsafe_allow_html=True)

# Analysis Button and Results
if st.button("🔍 Analyze and Get Recommendations", use_container_width=True):
    if scan_result and uploaded_pdf:
        with st.spinner("Processing with AI..."):
            response = llama_vision_detect(scan_result, report_text, feelings, location)
        
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Analysis and Recommendations")
        st.markdown(response)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-section">', unsafe_allow_html=True)
        st.warning("Please ensure you've uploaded both a scan image and a medical report.")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.sidebar.write("---")
st.markdown(
        "<3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/sanskar-khandelwal-611249210/'>Team code E Khiladi </a></3>",
        unsafe_allow_html=True
    )
# Optional: Add visitor counter if needed
# st.sidebar.markdown('''
#     <center>
#     <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" 
#     title="Free Counter" Alt="web counter" width="100" height="40" border="0" /></h1>
#     </center>
# ''', unsafe_allow_html=True)

