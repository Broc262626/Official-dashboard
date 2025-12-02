import streamlit as st
import pandas as pd
import os
from io import BytesIO
import streamlit_authenticator as stauth
import yaml

# ---------------------------
#  Authentication
# ---------------------------

# Sample credentials; replace with your own secure credentials
credentials = {
    "usernames": {
        "admin": {"name": "Admin User", "password": "admin123", "role": "admin"},
        "viewer": {"name": "Viewer User", "password": "viewer123", "role": "viewer"},
    }
}

# Authenticator setup
authenticator = stauth.Authenticate(
    credentials,
    "camera_dashboard_cookie",
    "camera_dashboard_session",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

# ---------------------------
# Initialize CSV
# ---------------------------

CSV_FILE = "repairs.csv"
COLUMNS = ["Server", "Depot name", "Fleet name", "Registration", "Issues", "Priority", "Tech comments"]

if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=COLUMNS)
    df.to_csv(CSV_FILE, index=False)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv(CSV_FILE)

# Save data
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# ---------------------------
# App
# ---------------------------

if authentication_status:
    st.set_page_config(page_title="Camera Health Repair Dashboard", layout="wide")
    
    st.markdown(
        """
        <style>
        .css-18e3th9 {background-color: #121212;}
        .css-1d391kg {color: orange;}
        .stButton>button {background-color: orange; color:black;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.title("📸 Camera Health Check Repair Dashboard")
    st.subheader(f"Welcome {name} ({credentials['usernames'][username]['role'].capitalize()})")
    
    df = load_data()

    # ---------------------------
    # Admin actions
    # ---------------------------
    if credentials["usernames"][username]["role"] == "admin":
        st.markdown("### Add New Vehicle Record")
        with st.form("add_form"):
            server = st.text_input("Server")
            depot = st.text_input("Depot Name")
            fleet = st.text_input("Fleet Name")
            reg = st.text_input("Registration")
            issues =
