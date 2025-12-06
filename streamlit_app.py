import streamlit as st
from dashboard import show_dashboard
from streamlit_authenticator import Authenticate
import yaml

with open('config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'sidebar')

if authentication_status:
    st.sidebar.write(f'Welcome *{name}*')
    show_dashboard()
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
