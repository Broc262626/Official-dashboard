import streamlit as st
import pandas as pd
import os
import streamlit_authenticator as stauth

credentials = {
    "usernames": {
        "admin": {"name": "Admin User", "password": "admin123", "role": "admin"},
        "viewer": {"name": "Viewer User", "password": "viewer123", "role": "viewer"},
    }
}

authenticator = stauth.Authenticate(credentials, "camera_dashboard_cookie", "camera_dashboard_session", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

CSV_FILE = "repairs.csv"
COLUMNS = ["Server", "Depot name", "Fleet name", "Registration", "Issues", "Priority", "Tech comments"]

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(CSV_FILE, index=False)

@st.cache_data
def load_data():
    return pd.read_csv(CSV_FILE)

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

if authentication_status:
    st.set_page_config(page_title="Camera Health Repair Dashboard", layout="wide")
    st.markdown("""<style>
        .css-18e3th9 {background-color: #121212;}
        .css-1d391kg {color: orange;}
        .stButton>button {background-color: orange; color:black;}
    </style>""", unsafe_allow_html=True)

    st.title("📸 Camera Health Check Repair Dashboard")
    st.subheader(f"Welcome {name} ({credentials['usernames'][username]['role'].capitalize()})")

    df = load_data()

    if credentials['usernames'][username]['role'] == 'admin':
        st.markdown("### Add New Vehicle Record")
        with st.form("add_form"):
            server = st.text_input("Server")
            depot = st.text_input("Depot Name")
            fleet = st.text_input("Fleet Name")
            reg = st.text_input("Registration")
            issues = st.text_input("Issues")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            tech_comments = st.text_area("Tech Comments")
            submitted = st.form_submit_button("Add Record")
            if submitted:
                new_row = pd.DataFrame([[server, depot, fleet, reg, issues, priority, tech_comments]], columns=COLUMNS)
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("Record added successfully!")

        st.markdown("### Import Records from Excel (Append)")
        uploaded_file = st.file_uploader("Choose Excel file", type=["xlsx"])
        if uploaded_file:
            excel_data = pd.read_excel(uploaded_file)
            missing_cols = [col for col in COLUMNS if col not in excel_data.columns]
            if missing_cols:
                st.error(f"Missing columns: {', '.join(missing_cols)}")
            else:
                df = pd.concat([df, excel_data[COLUMNS]], ignore_index=True)
                save_data(df)
                st.success("Excel data appended successfully!")

        st.markdown("### Edit/Delete Records")
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("Save Changes"):
            save_data(edited_df)
            st.success("Changes saved successfully!")

    st.markdown("### Camera Health Records")
    filter_depot = st.selectbox("Filter by Depot", ["All"] + sorted(df["Depot name"].unique()))
    filter_priority = st.selectbox("Filter by Priority", ["All"] + ["Low", "Medium", "High"])
    search_reg = st.text_input("Search Registration")

    filtered_df = df.copy()
    if filter_depot != "All":
        filtered_df = filtered_df[filtered_df["Depot name"] == filter_depot]
    if filter_priority != "All":
        filtered_df = filtered_df[filtered_df["Priority"] == filter_priority]
    if search_reg:
        filtered_df = filtered_df[filtered_df["Registration"].str.contains(search_reg, case=False)]

    st.dataframe(filtered_df, use_container_width=True)
    authenticator.logout("Logout", "sidebar")

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
