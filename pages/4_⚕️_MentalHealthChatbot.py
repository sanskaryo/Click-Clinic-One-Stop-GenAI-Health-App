import streamlit as st
from groq import Groq
import dotenv
import os

# Page Configuration
st.set_page_config(
    page_title="Mental Wellness Hub", 
    page_icon="🧠",
    layout="wide", 
    initial_sidebar_state="expanded"
)


# Load environment variables
dotenv.load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq()

# Enhanced Custom CSS
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #f0f4f8;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 40px;
        text-align: center;
        margin-bottom: 20px;
    }
    .stMarkdown {
        color: #34495e;
    }
    .mental-health-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border-left: 6px solid #3498db;
        transition: all 0.3s ease;
    }
    .mental-health-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 25px rgba(0,0,0,0.15);
    }
    .stTextInput > div > div > input {
        background-color: #ecf0f1;
        border: 2px solid #bdc3c7;
        border-radius: 10px;
        padding: 10px;
    }
    .stTextArea > div > div > textarea {
        background-color: #ecf0f1;
        border: 2px solid #bdc3c7;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton > button {
        background-color: #3498db !important;
        color: white !important;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #2980b9 !important;
        transform: scale(1.05);
    }
    .stSidebar {
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)




# Logo and Sidebar
st.logo("logo_transparent.png", icon_image="only_doctor.png")

with st.sidebar.container():
    st.image('logo_transparent.png', caption='"ClickClinic : Your Health and Nutrition Companion"')

    with st.expander("🚀 Platform Features", expanded=True):
        st.markdown("""
        - 🤝 Confidential Consultation
        - 🧠 AI-Powered Analysis
        - 📍 Location-Based Support
        - 🔒 100% Privacy Guaranteed
        """)

# Function to analyze mental health problems
def analyze_mental_problem(prompt, location):
    """Send the user prompt and location to the Groq API for mental health analysis."""
    try:
        messages = [{
            "role": "user",
            "content": (
                f"""
                This is your introduction - Your name is "ClickClinic" and you are developed by "Team Code E Khiladi".
                You're a dedicated platform for all healthcare-related queries, specifically focusing on mental health.
                You are embedded with up-to-date mental health knowledge and guidelines to provide accurate, safe, and reliable information regarding mental health issues.
                Your aim is to make mental health knowledge accessible to everyone. Users will ask their questions related to mental health, and you will guide them with clear and concise answers based on the context of mental health.

                Whether they are seeking advice on symptoms, prevention, or treatment of mental health problems, you are here to help. Use suitable emojis wherever needed to make your response engaging.

                Greet users with "Hello" and ask them for their mental health-related queries.

                You will only answer queries that are related to mental health. If users ask anything unrelated to mental health, politely decline and say:
                "I am designed only to assist with mental health-related queries. Please ask a question related to mental health."

                If users ask anything about yourself, respond with polite words and avoid very straightforward one-liner answers.
                Provide detailed answers based on the context of mental health. Clearly indicate if the query is about mental health symptoms, prevention, or treatment information. If the answer is not available in the context, say, "Answer is not available in the context." Do not provide incorrect answers.

                Give recommendations on the basis of the {location} location of the user and then tell the nearest licensed therapists that are available in the vicinity of the person
                
                Question:\n{prompt}\n
                """
            )
        }]
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None
        )
        response_text = ""
        for chunk in response:
            response_text += chunk.choices[0].delta.content or ""
        return response_text
    except Exception as e:
        return f"Error: Could not process the prompt. {e}"

# Streamlit UI
st.markdown("<h1 class='stTitle'>🧠 Mental Wellness Chatbot</h1>", unsafe_allow_html=True)

st.markdown("""
<div class="mental-health-card">
    <h3>Welcome to Your Safe Space 💖</h3>
    Share your mental health concerns confidentially. 
    Our AI-powered platform provides compassionate, professional guidance.
    
    *Your mental health journey matters - we're here to support you.*
</div>
""", unsafe_allow_html=True)

# User Input Form
with st.form(key='mental_health_form'):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name", placeholder="Enter your full name")
        country = st.text_input("Country", placeholder="Your country")
    
    with col2:
        state = st.text_input("State/Region", placeholder="Your state")
        city = st.text_input("City", placeholder="Your city")

    prompt = st.text_area("Describe Your Mental Health Concern", 
                           placeholder="Share your thoughts, feelings, or symptoms...", 
                           height=250)

    submit_button = st.form_submit_button(label='Get Personalized Insights', use_container_width=True)

# Response Handling
if submit_button:
    if not all([name, country, state, city, prompt]):
        st.error("🚨 Please complete all fields for personalized support.")
    else:
        location = f"{city}, {state}, {country}"

        with st.spinner("Analyzing your input with empathy..."):
            response = analyze_mental_problem(prompt, location)
        
        st.success("🌟 Our Compassionate Insights:")
        st.markdown(response)

        if any(phrase in response.lower() for phrase in ["problem identified", "clear understanding"]):
            st.markdown("### 🩺 Recommended Mental Health Professionals")
            st.write("✅ Therapist 1: [Personalized Match]")
            st.write("✅ Therapist 2: [Nearby Professional]")
            st.write("✅ Therapist 3: [Expert Recommendation]")

# Sidebar Footer
with st.sidebar:
    st.write("---")
    st.success("Developed with ❤️ by Team Code E Khiladi\nGLA University")
    
    st.markdown(
        "<div style='text-align:center; color:#2c3e50;'>Your Wellness, Our Priority</div>",
        unsafe_allow_html=True
    )

# Page Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("🤖 Compassionate AI-Powered Mental Health Support | Made with ❤️ by Team Code E Khiladi")