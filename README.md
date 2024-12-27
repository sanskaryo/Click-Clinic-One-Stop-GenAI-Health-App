# ClickClinic: Your AI-Powered Health and Nutrition Companion

Welcome to **ClickClinic**, an AI-powered healthcare platform designed to provide comprehensive health and nutrition solutions. Developed by **Team Manthan**, this project leverages open-source large language models (LLMs) and various tech stacks to offer a one-stop solution for all your health and nutrition needs.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

ClickClinic is an AI-powered healthcare platform that aims to simplify healthcare access and empower users with AI-driven insights. From finding nearby health services to managing reminders and providing 24/7 assistance, ClickClinic ensures that your healthcare is just a click away.

## Features

- **Find Doctor**: Locate nearby doctors and healthcare services based on your current location.
- **Reminder Bot**: Automate and manage reminders for medications, appointments, and check-ups.
- **WhatsApp Bot Integration**: Get 24/7 assistance and quick responses to your health queries via WhatsApp.
- **ClickClinic on Call**: Call for personalized health advice and assistance directly over the phone.
- **Label Scanner**: Analyze food labels to determine their health rating, safety for consumption, and suitability for children and diabetics.
- **Calorie Counter**: Calculate the total calories of food items from an image and provide detailed nutritional information.
- **Mental Health Chatbot**: Get compassionate, professional guidance on mental health concerns.
- **Prescription Reader**: Instantly analyze prescriptions and lab reports with AI.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, Google Generative AI, Twilio API, PDFPlumber, PIL, Requests
- **APIs**: Google Generative AI, Twilio API, Groq API
- **Libraries**: Streamlit, Streamlit-Lottie, Streamlit-Option-Menu, Streamlit-WebRTC, Langchain, PDFPlumber, PIL, Requests, Pyrebase, Firebase-Admin, TensorFlow, SpeechRecognition, gTTS, TQDM, Protobuf, PyPDF2, Pyrebase4, OAuth2Client, Faiss-CPU

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/ClickClinic.git
    cd ClickClinic
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory and add the following variables:
    ```env
    GROQ_API_KEY="your_groq_api_key_here"
    OPENAI_API_KEY="your_openai_api_key_here"
    HF_TOKEN="your_hf_token_here"
    LANGCHAIN_API_KEY="your_langchain_api_key_here"
    GOOGLE_API_KEY="your_google_api_key_here"
    account_sid="your_account_sid_here"
    auth_token="your_auth_token_here"
    twilio_number="your_twilio_number_here"
    ```

## Usage

1. Run the Streamlit application:
    ```sh
    streamlit run Main.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to access ClickClinic.

## Project Structure

- **.env.example**: Example environment variables file.
- **.gitattributes**: Git attributes file.
- **.gitignore**: Git ignore file to exclude certain files from being tracked.
- **Main.py**: Main script to run the application.
- **pages/**: Directory containing various functionalities of the application:
  - **.env**: Environment variables file for the pages.
  - **1_📜HealthDecoder.py**: Script for decoding health-related information.
  - **12🏥FindDoctor.py**: Script for finding doctors.
  - **2🧃LabelScanner.py**: Script for scanning labels.
  - **3🥕CalorieCounter.py**: Script for counting calories.
  - **4⚕️MentalHealthChatbot.py**: Script for the mental health chatbot.
  - **4🔔Reminder.py**: Script for setting reminders.
  - **5📝_PrescriptionReader.py**: Script for reading prescriptions.
  - **cities.json**: JSON file containing city data.
- **README.md**: This file, containing information about the project.
- **requirements.txt**: List of dependencies required for the project.


## Contributing

We welcome contributions from the community! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your fork.
5. Open a pull request to the main repository.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements

- **Team Manthan**: 2nd Year Students, B.Tech CSE  GLA University
- Special thanks to all the open-source contributors and the developers of the libraries and APIs used in this project.

---

Developed with ❤️ by [Team Manthan](https://www.linkedin.com/in/sanskar-khandelwal-611249210/) at AI Chat Hackathon.
