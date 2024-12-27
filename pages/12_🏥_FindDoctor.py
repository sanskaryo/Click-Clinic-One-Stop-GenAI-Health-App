import requests
import json
import streamlit as st
import math
import os

# --- Page Config ---
st.set_page_config(
    page_title="Healthcare Services Finder",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo("logo_transparent.png", icon_image="only_doctor.png")

# --- Header ---
st.title("🏥 Find Healthcare Services Near You")
st.markdown('####')

def print_praise():
        praise_quotes = """
        Team Code e khiladi

    2nd Year Students,
    B.Tech CSE AIML (2023-2027),
    GLA UNIVERSITY
        """
        title = "**Developed By -**\n\n"
        return title + praise_quotes

# Sidebar
with st.sidebar.container():
    st.image('logo_transparent.png', caption='ClickClinic : Your Health, Just a Click Away 🏥')

    # Features in an expander
    with st.expander("🚀 Features", expanded=False):
        st.markdown("- Search for Healthcare Services by Type")
        st.markdown("- Find Services Near You by State and City")
        st.markdown("- Customizable Search Radius")

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
    .service-name {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 10px;
        color: #2c3e50;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .service-address {
        font-size: 14px;
        color: #7f8c8d;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
    }
    .slider-label {
        font-size: 30px;
        font-weight: bold;
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
    .custom-selectbox {
        border: 2px solid #4A90E2;
        border-radius: 5px;
        padding: 5px;
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

# State code mapping
state_code_mapping = {
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CT": "Chhattisgarh",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "HP": "Himachal Pradesh",
    "JK": "Jammu and Kashmir",
    "JH": "Jharkhand",
    "KA": "Karnataka",
    "KL": "Kerala",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "MN": "Manipur",
    "ML": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OR": "Odisha",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TG": "Telangana",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "UT": "Uttarakhand",
    "WB": "West Bengal",
    "AN": "Andaman and Nicobar Islands",
    "CH": "Chandigarh",
    "DH": "Dadra and Nagar Haveli and Daman and Diu",
    "DL": "Delhi",
    "LD": "Lakshadweep",
    "PY": "Puducherry",
    "LA": "Ladakh"
}

# Load city data
with open(r'pages\cities.json', 'r') as f:
    city_data = json.load(f)

# Create a set of unique states
states = sorted({state_code_mapping.get(city['stateCode'], city['stateCode']) for city in city_data})

# Streamlit UI
st.sidebar.write("---")
st.sidebar.markdown('<div class="title">Healthcare Services Finder</div>', unsafe_allow_html=True)

# Create three columns for the search interface
col1, col2, col3 = st.columns(3)

# State selection
with col1:
    selected_state = st.selectbox("Select State", ["Select a state"] + states, index=0, key="state_select")

# City selection
with col2:
    if selected_state and selected_state != "Select a state":
        selected_state_code = next((code for code, name in state_code_mapping.items() if name == selected_state), None)
        filtered_cities = [city['name'] for city in city_data if city['stateCode'] == selected_state_code]
        selected_city = st.selectbox("Select City", ["Select a city"] + filtered_cities, index=0, key="city_select")
    else:
        selected_city = st.selectbox("Select City", ["Select a city"], disabled=True, key="city_select_disabled")

# Healthcare service type input
with col3:
    service_type = st.text_input("Enter Healthcare Service Type", 
                                placeholder="Dentist, Hospital or Health ",
                                help="Enter the type of healthcare service you're looking for")

if selected_city and selected_city != "Select a city" and service_type:
    city_info = next((city for city in city_data if city['name'] == selected_city), None)

    if city_info:
        latitude = city_info['latitude']
        longitude = city_info['longitude']

        st.markdown('<div class="slider-label">Select search radius (in meters)</div>', unsafe_allow_html=True)
        radius_meters = st.slider('', 10000, 200000, 60000)
        radius_km = radius_meters / 1000
        st.write(f"Searching within a radius of {radius_km:.2f} km")

        if st.button('Search Healthcare Services', use_container_width=True):
            api_key = os.getenv('OLA_API_KEY')
            api_url = ""
            
            params = {
                "layers": "{}",
                "types": service_type,
                "location": f"{latitude},{longitude}",
                "radius": radius_meters,
                "api_key": api_key,
                "limit": 50
            }

            try:
                response = requests.get(api_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()

                    if 'predictions' in data and data['predictions']:
                        st.subheader(f"Healthcare services found within {radius_km:.2f} km:")
                        st.markdown("---")

                        num_services = len(data['predictions'])
                        num_rows = math.ceil(num_services / 3)

                        for row in range(num_rows):
                            cols = st.columns(3)
                            for col in range(3):
                                service_index = row * 3 + col
                                if service_index < num_services:
                                    service = data['predictions'][service_index]
                                    with cols[col]:
                                        search_query = f"{service['structured_formatting']['main_text']} {selected_city}"
                                        google_search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                                        st.markdown(f"""
                                        <a href="{google_search_url}" target="_blank" style="text-decoration: none;">
                                            <div class="service-card"> 
                                                <div class="service-name">{service['structured_formatting']['main_text']}</div>
                                                <div class="service-address">{service['structured_formatting']['secondary_text']}</div>
                                            </div>
                                        </a>
                                        """, unsafe_allow_html=True)
                        st.markdown("---")
                    else:
                        st.warning(f"No healthcare services found within {radius_km:.2f} km.")
                else:
                    st.error(f"Error: Unable to fetch data (Status Code: {response.status_code})")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Sidebar footer
with st.sidebar:
    st.write("---")
    st.success(print_praise())
    st.write("---")
    
    st.markdown(
        "<h3 style='text-align: center;'>Developed with ❤️ for GenAI by <a style='text-decoration: none' href='https://www.linkedin.com/in/sanskar-khandelwal-611249210/'>Team Code E Khiladi</a></h3>",
        unsafe_allow_html=True
    )

    st.markdown('''
        <center>
        <h1>Visitors Count : <img src="https://counter8.optistats.ovh/private/freecounterstat.php?c=b2j4e593kabemp2m8eww4c4m63e339lu" title="Free Counter" Alt="web counter" width="100" height="40"  border="0" /></h1>
        </center>
    ''', unsafe_allow_html=True)