import streamlit as st
import os
import requests
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

load_dotenv()


st.set_page_config(
    page_title="ClickClinic",
    layout="wide",
    page_icon="🏥"
)


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_health_bot = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_qmfs6c3i.json")
lottie_reminder = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_xh83pj1c.json")
lottie_find_doctor = load_lottieurl("https://lottie.host/80b5b580-97c7-48f5-a0e6-565dfb86498a/y2ZzX3B4bB.json")
lottie_call_support = load_lottieurl("https://assets4.lottiefiles.com/private_files/lf30_jcikwtux.json")


translations = {
    "English": {
        "welcome": "ClickClinic: Your AI Healthcare and Nutrition Companion",
        "chat_placeholder": "Ask your health-related query here...",
        "thinking": "Thinking...",
        "new_chat": "Start a New Chat",
        "label_chat": "Label your chat:",
        "save_label": "Save Chat Label",
    },
    "Hindi": {
        "welcome": "क्लिकक्लिनिक में आपका स्वागत है: आपका AI स्वास्थ्य साथी",
        "chat_placeholder": "अपना स्वास्थ्य से संबंधित प्रश्न यहाँ पूछें...",
        "thinking": "सोच रहा हूँ...",
        "new_chat": "नई चैट शुरू करें",
        "label_chat": "अपनी चैट को लेबल करें:",
        "save_label": "चैट लेबल सहेजें",
    },
    
}


with st.sidebar:
    st.image('logo_transparent.png', caption="ClickClinic: Your Health, Just a Click Away 🏥")
    
    # # Language selector
    # languages = list(translations.keys())
    # st.session_state.language = "English"
    # selected_language = st.sidebar.selectbox("Select Language 🌐", languages, index=languages.index(st.session_state.get('language', 'English')))
    # if selected_language != st.session_state.get('language', 'English'):
    #     st.session_state.language = selected_language
    #     st.rerun()
    
    # About Us
    with st.sidebar.expander("ℹ️ About Us", expanded=False):
        st.markdown("ClickClinic: Your AI Healthcare and Nutrition Companion")
        st.success("AI-powered healthcare assistant for your well-being.")

    # Features
    with st.sidebar.expander("🚀 Features", expanded=False):
        st.markdown("- **Find Doctor**: Locate nearby healthcare services.\n"
                    "- **Reminder Bot**: Automates healthcare reminders.\n"
                    "- **WhatsApp Bot Integration**: For 24/7 health assistance.\n"
                    "- **ClickClinic on Call**: Personalized advice via phone.")
        
    st.write("--------------")
    
    st.markdown(
        "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/sanskar-khandelwal-611249210/'>Team Code E Khiladi</a></h3>",
        unsafe_allow_html=True
    )

    st.write("--------------")

    # st.markdown('''<center>
    #     <h1>Visitors Count : 
    #     <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40" border="0" />
    #     </h1></center>''', unsafe_allow_html=True)


st.title("ClickClinic: Your AI Healthcare and Nutrition Companion")


tab1, tab2, tab3 = st.tabs(["About", "Features", "Get Started"])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        # About ClickClinic

        **ClickClinic** is your all-in-one AI-powered healthcare platform. It offers smart solutions to enhance your health journey. From finding nearby health services to managing reminders and providing 24/7 assistance, ClickClinic ensures that your healthcare is just a click away. 🌟

        Our mission is to simplify healthcare access and empower you with AI-driven insights to stay healthy and informed.
        """)
    with col2:
        st_lottie(lottie_health_bot, height=300, key="health-bot")

with tab2:
    st.header("Key Features of ClickClinic")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        - **🩺 Find Doctor**: Locate nearby doctors and healthcare services based on your current location.
        - **⏰ Reminder Bot**: Automate and manage reminders for medications, appointments, and check-ups.
        - **📱 WhatsApp Bot Integration**: Get 24/7 assistance and quick responses to your health queries via WhatsApp.
        - **📞 ClickClinic on Call**: Call for personalized health advice and assistance directly over the phone.
        """)
    with col2:
        st_lottie(lottie_reminder, height=400, key="reminder")

with tab3:
    st.header("Get Started with ClickClinic")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        1. **Choose a feature** to get started:
            - Locate doctors using the "Find Doctor" option
            - Set up automated health reminders
            - Connect with our WhatsApp Bot for quick help
            - Call for personalized advice
        2. **Select your preferred language** for a personalized experience.
        3. **Login or Sign Up** to access all features and save your interaction history.
        4. Experience AI-powered healthcare like never before!
        """)
        
        # if st.button("Launch ClickClinic 🚀"):
        #     st.success("Redirecting to ClickClinic services...")
        #     # Add actual redirection logic here
    with col2:
        st_lottie(lottie_find_doctor, height=400, key="get-started")


st.markdown("""
<div style="background-color:#ffcccb; padding:20px; border-radius:10px; border: 2px solid red; margin-top: 30px;">
    <h4 style="color:red; font-weight:bold;">⚠️ Important Notice</h4>
    <p style="color:black;">ClickClinic is an AI-powered healthcare platform that provides general health advice and assistance. While we aim for accuracy, the platform does not replace professional medical consultation. Please consult a qualified healthcare professional for any serious health concerns or emergencies.</p>
</div>
""", unsafe_allow_html=True)


st.markdown("""
---
<p style="text-align: center;">© 2024 ClickClinic - AI Healthcare Companion. All rights reserved.</p>
""", unsafe_allow_html=True)
