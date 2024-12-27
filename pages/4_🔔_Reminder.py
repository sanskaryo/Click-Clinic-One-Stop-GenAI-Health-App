import streamlit as st
from datetime import datetime, time
import pytz
import schedule
import time as t
import threading
from twilio.rest import Client
import google.generativeai as genai

# Replace these with your actual credentials
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_WHATSAPP_NUMBER = ''
TWILIO_SMS_NUMBER = ''
USER_WHATSAPP_NUMBER = ''
USER_SMS_NUMBER = ''

# Replace with your actual Gemini API key
GEMINI_API_KEY = ''

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# IST timezone
IST = pytz.timezone('Asia/Kolkata')

# Initialize session state
if "reminders" not in st.session_state:
    st.session_state.reminders = []

if "scheduler_started" not in st.session_state:
    st.session_state.scheduler_started = False

# Function to generate a health fact
def generate_health_fact():
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = "Generate a short, interesting health fact or health tip that would be motivational and informative. Keep it concise (1-2 sentences)."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating health fact: {e}")
        return "Stay hydrated and active for better health!"

# CSS Styling (same as previous code)
st.markdown("""
    <style>
    .title {
        text-align: left;
        font-size: 35px;
        font-weight: bold;
        color: black;
    }
    .service-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
        border-left: 5px solid #3498db;
        cursor: pointer;
    }
    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 10px 16px 18px rgba(0, 0, 0, 0.15);
        background-color: #f0f8ff;
    }
    .custom-selectbox {
        border: 2px solid #4A90E2;
        border-radius: 5px;
        padding: 5px;
        background-color: white;
    }
    .search-button {
        background-color: #3498db;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
        display: block;
        text-align: center;
    }
    .search-button:hover {
        background-color: #2980b9;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar configuration
st.logo("logo_transparent.png", icon_image="only_doctor.png")
with st.sidebar.container():
    st.image('logo_transparent.png', caption='ClickClinic : Your Health, Just a Click Away 🏥')

    # Features in an expander
    with st.expander("🚀 Features", expanded=False):
        st.markdown("- Create Health Reminders")
        st.markdown("- Multiple Notification Channels")
        st.markdown("- Daily Health Facts")

# Function to send a WhatsApp message
def send_whatsapp_message(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=USER_WHATSAPP_NUMBER
        )
        print(f"WhatsApp message sent: {message}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

# Function to send an SMS message
def send_sms_message(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_SMS_NUMBER,
            to=USER_SMS_NUMBER
        )
        print(f"SMS message sent: {message}")
    except Exception as e:
        print(f"Error sending SMS message: {e}")

# Function to trigger a reminder
def trigger_reminder(reminder):
    # Generate a health fact
    health_fact = generate_health_fact()
    
    message = reminder["message"]
    reminder_time = reminder["datetime"].strftime('%Y-%m-%d %H:%M:%S %Z')
    full_message = f"⏰ Reminder Alert! 📅\nMessage: {message}\nTime: {reminder_time}\n\n💡 Health Tip: {health_fact}"
    
    # Send notifications based on the selected options
    if "WhatsApp" in reminder["channels"]:
        send_whatsapp_message(full_message)
    if "SMS" in reminder["channels"]:
        send_sms_message(full_message)

# Schedule a reminder
def schedule_reminder(reminder):
    def job():
        # Check if the reminder is "Once" and already triggered
        if reminder["frequency"] == "Once" and reminder["triggered"]:
            return schedule.CancelJob  # Cancel the job if already triggered

        # Trigger the reminder
        trigger_reminder(reminder)

        # Mark one-time reminder as triggered and cancel the job
        if reminder["frequency"] == "Once":
            reminder["triggered"] = True
            return schedule.CancelJob

    # Schedule based on frequency
    reminder_time = reminder["datetime"].strftime('%H:%M')
    if reminder["frequency"] == "Daily":
        schedule.every().day.at(reminder_time).do(job)
    elif reminder["frequency"] == "Weekly":
        schedule.every().week.at(reminder_time).do(job)
    elif reminder["frequency"] == "Once":
        # Schedule for a one-time trigger
        schedule.every().day.at(reminder_time).do(job)

    print(f"Scheduled: {reminder['message']} at {reminder['datetime']} ({reminder['frequency']})")

# Run the scheduler in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        t.sleep(1)

if not st.session_state.scheduler_started:
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    st.session_state.scheduler_started = True

# Streamlit UI
st.title("⏰ Health Care Assistant - Reminder Setup   \n")
st.write("Set up reminders to receive notifications via WhatsApp, SMS, or both. All times are in IST.")

# Input fields with custom styling
col1, col2 = st.columns(2)

with col1:
    reminder_message = st.text_input("Enter the reminder message", "")
    reminder_date = st.date_input("Enter the reminder date", min_value=datetime.now().date())

with col2:
    # Replace text input with time input
    reminder_time = st.time_input("Select reminder time", value="now", step=60)
    reminder_frequency = st.selectbox("Select Repeat Frequency", ["Once", "Daily", "Weekly"])

reminder_channels = st.multiselect("Select Notification Channels", ["WhatsApp", "SMS"], default=["WhatsApp"])

# Validation and confirmation button with custom styling
if st.button("Set Reminder", use_container_width=True, help="Click to schedule your health reminder"):
    # Validation logic
    if not reminder_message:
        st.error("Please enter a reminder message.")
    elif not reminder_time:
        st.error("Please enter a valid time in HH:MM format.")
    elif not reminder_channels:
        st.error("Please select at least one notification channel.")
    else:
        # Combine date and time
        reminder_datetime = datetime.combine(reminder_date, reminder_time).astimezone(IST)

        if reminder_datetime <= datetime.now(IST):
            st.error("Reminder time must be in the future.")
        else:
            reminder = {
                "message": reminder_message,
                "datetime": reminder_datetime,
                "frequency": reminder_frequency,
                "channels": reminder_channels,
                "triggered": False
            }
            st.session_state.reminders.append(reminder)
            
            schedule_reminder(reminder)

            # Success message
            st.success(f"Reminder set successfully! 📅\nMessage: '{reminder_message}'\nTime: {reminder_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')}\nFrequency: {reminder_frequency}\nChannels: {', '.join(reminder_channels)}")
            
            # Send confirmation notifications
            for channel in reminder_channels:
                confirmation_message = f"✅ Reminder Created!\nMessage: '{reminder_message}'\nTime: {reminder_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')}\nFrequency: {reminder_frequency}"
                
                # Also include a health fact in the confirmation
                health_fact = generate_health_fact()
                confirmation_message += f"\n\n💡 Health Tip: {health_fact}"
                
                if channel == "WhatsApp":
                    send_whatsapp_message(confirmation_message)
                if channel == "SMS":
                    send_sms_message(confirmation_message)

# Display active reminders
if st.session_state.reminders:
    st.subheader("📋 Scheduled Reminders:")
    for idx, reminder in enumerate(st.session_state.reminders, 1):
        st.write(f"**{idx}.** {reminder['message']} - {reminder['datetime'].strftime('%Y-%m-%d %H:%M:%S %Z')} ({reminder['frequency']}) via {', '.join(reminder['channels'])}")

def print_praise():
        praise_quotes = """
        Team Code E Khiladi

    2nd Year Students,
    B.Tech CSE (AIML & IOT)
    GLA UNIVERSITY
        """
        title = "**Developed By -**\n\n"
        return title + praise_quotes

# Sidebar footer
with st.sidebar:
    st.write("---")
    st.success(print_praise())
    st.write("---")
    
    st.markdown(
        "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/sanskar-khandelwal-611249210/'>Team Manthan</a></h3>",
        unsafe_allow_html=True
    )

    # st.markdown('''
    #     <center>
    #     <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40"  border="0" /></h1>
    #     </center>
    # ''', unsafe_allow_html=True)