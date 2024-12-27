
from dotenv import load_dotenv

load_dotenv()  

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(image):
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = """
    You are an expert nutritionist. Analyze the food label from the image and provide the following information:
    1. Health rating out of 10.
    2. Whether it is healthy or not.
    3. Is it safe for average consumption?
    4. Important constituents.
    5. Presence of any harmful chemicals.
    6. Sugar content.
    7. Whether it is suitable for children and diabetics.
    Keep the answer concise and not very long.
    """
    response = model.generate_content([image[0], prompt])
    return response.text

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
        raise FileNotFoundError("No file uploaded")


def input_image_from_camera(image_data):
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        }
    ]
    return image_parts


st.set_page_config(page_title="Label Reader Health App")


st.title("Label Reader Health App 🧑‍⚕️")
st.markdown("""
Welcome to the Label Reader Health App! This app allows you to analyze food labels to determine their health rating, safety for consumption, and suitability for children and diabetics. You can either upload an image of a food label or capture one using your device's camera.

### How to Use:
1. **Upload an Image**: Click on the "Choose an image..." button to upload an image of a food label.
                                        **OR**
   **Capture an Image**: Use the camera feature to capture an image of a food label.
3. **Analyze**: Click on the "Analyze Label" button to get the health analysis of the food label.

The app will provide a health rating out of 10, indicate whether the food is healthy, list important constituents, and more.
""")


uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])


st.markdown("<h3 style='text-align: center;'>OR</h3>", unsafe_allow_html=True)

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.image_data = None

    def transform(self, frame):
        self.image_data = frame.to_ndarray(format="bgr24")
        return frame

webrtc_ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
elif webrtc_ctx.video_transformer:
    if webrtc_ctx.video_transformer.image_data is not None:
        image = webrtc_ctx.video_transformer.image_data
        st.image(image, caption="Captured Image.", use_column_width=True)

submit = st.button("Analyze Label")


if submit:
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
    elif webrtc_ctx.video_transformer and webrtc_ctx.video_transformer.image_data is not None:
        image_data = input_image_from_camera(webrtc_ctx.video_transformer.image_data)
    else:
        st.error("No image provided")
        image_data = None

    if image_data:
        response = get_gemini_response(image_data)
        st.subheader("The Response is")
        st.write(response)

# Footer
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>Made with ❤️ by Sanskar</p>
    </div>
    """, unsafe_allow_html=True)

def developer():
    st.markdown(
        "<h3 style='text-align: center;'>Developed with ❤️  <a style='text-decoration: none' href='https://www.linkedin.com/in/sanskar-khandelwal-611249210/'>Team Code E Khiladi</a></h3>",
        unsafe_allow_html=True
    )

# Function to print developer information
def print_praise():
    praise_quotes = """
    Team Code E Khiladi

    2nd Year Students,
    B.Tech CSE(AIML & IOT) CA
    GLA UNIVERSITY
    """
    title = "**Developed By -**\n\n"
    return title + praise_quotes
