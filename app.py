
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Camera Repairs Dashboard", layout="wide")

st.markdown("<h1 style='color:orange;'>Camera Health Check – Repairs Dashboard</h1>", unsafe_allow_html=True)

def login():
    st.sidebar.title("Login")
    user = st.sidebar.text_input("Username")
    pw = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if user == "admin" and pw == "admin123":
            return "admin"
        elif user == "viewer" and pw == "viewer123":
            return "viewer"
        else:
            st.sidebar.error("Invalid login")
            return None
    return None

role = login()
if not role:
    st.stop()

df = pd.read_csv("repairs.csv")

st.subheader("Repairs Table")

search = st.text_input("Search registration or issue")

tbl = df.copy()
if search:
    tbl = tbl[tbl.apply(lambda r: search.lower() in r.astype(str).str.lower().to_string(), axis=1)]

st.dataframe(tbl, use_container_width=True)

if role == "admin":
    st.subheader("Add New Record")
    with st.form("add"):
        s = st.text_input("Server")
        d = st.text_input("Depot")
        f = st.text_input("Fleet")
        r = st.text_input("Registration")
        i = st.text_input("Issue")
        p = st.selectbox("Priority", ["Low","Medium","High"])
        c = st.text_area("Tech Comments")
        if st.form_submit_button("Add"):
            new = pd.DataFrame([[s,d,f,r,i,p,c]], columns=df.columns)
            df = pd.concat([df, new], ignore_index=True)
            df.to_csv("repairs.csv", index=False)
            st.success("Added record")

st.markdown("<br><br><i>Theme: Black & Orange</i>", unsafe_allow_html=True)
