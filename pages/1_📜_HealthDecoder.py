import os
import time
import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from audio_recorder_streamlit import audio_recorder
import base64
import textwrap

# Load environment variables
load_dotenv()

# Global variables
model = None
groq_api_key = os.getenv('GROQ_API_KEY')

# Prompt Template
prompt_template = ChatPromptTemplate.from_template(
    """
    This is your introduction - Your name is "ClickClinic" and you are developed by "Manthan".
    
    You're a dedicated platform for all healthcare-related queries. You are embedded with up-to-date medical knowledge and guidelines to provide accurate, safe, and reliable health information.
    
    Your aim is to make healthcare knowledge accessible to everyone. Users will ask their questions, and you will guide them with clear and concise answers based on the context of healthcare.
    
    Whether they are seeking advice on symptoms, prevention, or general health tips, you are here to help. Use suitable emojis wherever needed to make your response engaging.
    
    Greet users with "Namaste " and ask them for their healthcare-related queries.
    
    You will never answer questions outside the scope of healthcare. If users ask anything unrelated to healthcare, politely decline and say: 
    "I am designed only to assist with healthcare-related queries. Please ask a question related to health."
    
    If users ask anything about yourself, respond with polite words and avoid very straightforward one-liner answers.
    
    Provide detailed answers based on the context. Clearly indicate if the query is about general health, symptoms, prevention, or treatment information. If the answer is not available in the context, say, "Answer is not available in the context." Do not provide incorrect answers.
    
    IMPORTANT: You must respond ONLY in the {language} language. Do not use any other language in your response.
    
    If the language is Hindi, use Devanagari script exclusively. Avoid using English words or Roman script in your Hindi responses.
    
    Context:\n{context}\n
    Question: \n{input}\n
    
    Answer (in {language}):
    """
)

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Function to load the Groq model
def load_model():
    global model
    model = ChatGroq(groq_api_key=groq_api_key,
                     model_name="Llama-3.1-70b-versatile")

# Main function
def main():
    global model, groq_api_key

    # Set up Streamlit page
    st.set_page_config(page_title='ClickClinic', layout='wide', page_icon="🩺")
    st.sidebar.title("ClickClinic : Your Health and Nutrition Companion")
    
    # Initialize session state variables if not exist
    if 'audio_response' not in st.session_state:
        st.session_state.audio_response = False
    if 'messages' not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Namaste 🙏 How can I help you with your health query today?"}]
    
    # Sidebar setup
    setup_sidebar()

    # Handle user input and generate responses
    handle_user_input()

# Function to set up the sidebar
def setup_sidebar():
    with st.sidebar:
        st.image('logo_transparent.png', caption='"ClickClinic : Your Health and Nutrition Companion"')
        
        # Language selector
        languages = ["English", "Hindi"]
        language_code_mapping = {
            "English": "en-IN",
            "Hindi": "hi-IN"
        }

        selected_language = st.sidebar.selectbox("Select Language 🌐", languages, index=languages.index(st.session_state.get('language', 'English')))
        st.session_state.language = selected_language
        st.session_state.selected_language_code = language_code_mapping[selected_language]

        # About Us section
        with st.sidebar.expander("ℹ️ About Us", expanded=False):
            st.markdown("Welcome to ClickClinic, your AI-powered healthcare and nutrition assistant.")
            st.success("Personalized health guidance at your fingertips.")

        # Features section
        with st.sidebar.expander("🚀 Features", expanded=False):
            st.markdown("- AI-driven health insights\n- Multilingual support\n- Comprehensive health information")

        st.write("---")

        # Lottie animation
        lottie_url = "https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json"
        st_lottie(load_lottieurl(lottie_url), height=200, key="sidebar_animation")

        st.markdown("---")

        # Audio Upload
        st.write("#")
        st.write(f"### **🎤 Voice Input**")

        audio_prompt = None
        audio_file_added = False

        if "prev_speech_hash" not in st.session_state:
            st.session_state.prev_speech_hash = None

        speech_input = audio_recorder("Press to talk:", icon_size="3x", neutral_color="#6ca395")
        if speech_input and st.session_state.prev_speech_hash != hash(speech_input):
            st.session_state.prev_speech_hash = hash(speech_input)

            with open(f"temp_audio.wav", "wb") as f:
                f.write(speech_input)

            audio_prompt = speech2text()['transcript']
            st.session_state.audio_prompt = audio_prompt

        # Audio output toggle
        st.session_state.audio_response = st.toggle("Output Audio response", value=st.session_state.audio_response)

        st.markdown("---")

        # API key input fields
        setup_api_keys()

        st.markdown("---")

        st.success(print_praise())   
        st.write("---")

# Function to set up API keys
def setup_api_keys():
    global groq_api_key

    groq_api_key = os.environ['GROQ_API_KEY']
    # if groq_api_key:
    #     st.success('GROQ API key already provided!', icon='✅')
    # else:
    #     groq_api_key = st.text_input('Enter GROQ API Key:', type='password')
    #     if not (groq_api_key.startswith('gsk_') and len(groq_api_key)==56):
    #         st.warning('Please enter your GROQ API key!', icon='⚠️')
    #     else:
    #         os.environ['GROQ_API_KEY'] = groq_api_key
    #         st.success('GROQ API key accepted!', icon='👍')

    if groq_api_key:
        load_model()

# Function to handle user input and generate responses
def handle_user_input():
    # Retrieve existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Sidebar developer info
    with st.sidebar:
        developer()
    
    # User input
    if user_question := st.chat_input("Ask your health-related question...") or st.session_state.get('audio_prompt'):
        user_question = user_question or st.session_state.audio_prompt
        
        # Clear audio prompt after use
        if 'audio_prompt' in st.session_state:
            del st.session_state.audio_prompt
        
        st.session_state.messages.append({"role": "user", "content": user_question})
        
        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Processing your health query..."):
                # Generate response
                start = time.process_time()
                response = model.invoke(prompt_template.format(
                    context="Healthcare general knowledge", 
                    input=user_question, 
                    language=st.session_state.language
                )).content
                print("Response time:", time.process_time() - start)

                # Force Hindi response if Hindi is selected
                if st.session_state.language == "Hindi":
                    st.session_state.selected_language_code = "hi-IN"
                    response = f"निम्नलिखित उत्तर हिंदी में है:\n\n{response}"

                st.write(response)
                
                # Optional audio response
                if st.session_state.audio_response:
                    try:
                        sarvam(response, st.session_state.selected_language_code)
                    except Exception as e:
                        st.error(f"Audio generation failed: {e}")

                # Append assistant's message
                st.session_state.messages.append({"role": "assistant", "content": response})

# Rest of the functions remain the same as in the previous version...

# Sarvam AI speech to text function
def speech2text():
    url = ""
    payload = {
        "language_code": "hi-IN",
        "model": "",
        "with_timestamps": "false"
    }
    files = {
        'file': ('audio_file', open("temp_audio.wav", 'rb'),'audio/wav')
    }
    headers = {
        "api-subscription-key": "",
    }
    response = requests.post(url, files=files, data=payload, headers=headers)
    return response.json()

# Sarvam AI text to speech function
def sarvam(text, language_code):
    url = ""
    headers = {'API-Subscription-Key': '', "Content-Type": "application/json"}
    
    delimiters = "|" if language_code == "hi-IN" else "."
    segments = [segment.strip() for segment in text.split(delimiters) if segment.strip()]

    progress_bar = st.progress(0)
    total_steps = len(segments)
    output_file = "output.wav"
    
    with open(output_file, "wb") as audio_file:
        for i, segment in enumerate(segments):
            if len(segment) > 500:
                chunks = textwrap.wrap(segment, 500)
            else:
                chunks = [segment]

            for chunk in chunks:
                payload = {
                    "inputs": [chunk],
                    "target_language_code": language_code,
                    "speaker": "{}",
                    "pitch": 0,
                    "pace": 1.00,
                    "loudness": 1.15,
                    "speech_sample_rate": 8000,
                    "enable_preprocessing": True,
                    "model": "bulbul:v1"
                }

                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    try:
                        audio_string = response.text[12:-3]
                        audio_data = base64.b64decode(audio_string)
                        audio_file.write(audio_data)
                    except Exception as e:
                        st.error(f"Error decoding audio: {e}")
                        return
                else:
                    st.error(f"API request failed: {response.status_code}. Reason: {response.text}")
                    return

                time.sleep(0.5)

            progress_bar.progress((i + 1) / total_steps)

    # Display audio player without auto-play to prevent disruption
    st.audio(output_file, format="audio/wav")

# Developer function
def developer():
    st.markdown(
        "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/sanskar-khandelwal-611249210/'>Team Manthan At AI Chat Hackathon</a></h3>",
        unsafe_allow_html=True
    )

# Function to print developer information
def print_praise():
    praise_quotes = """
    Team Manthan:

    2nd Year Students,
    B.Tech CSE
    GLA UNIVERSITY
    """
    title = "**Developed By -**\n\n"
    return title + praise_quotes

# Run the main function
if __name__ == "__main__":
    main()