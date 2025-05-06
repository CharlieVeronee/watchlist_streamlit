import streamlit as st
from utils.auth import check_password, get_user_password
from sqlalchemy import text

st.title("Log In / Log Out")

if "app_username" not in st.session_state:
    st.session_state.app_username = None

if not st.session_state.app_username:
    with st.form("login-form"):
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        login = st.form_submit_button("Log In")

        if login:
            stored_hash = get_user_password(username_input.strip())
            if stored_hash and check_password(password_input, stored_hash):
                st.session_state.app_username = username_input.strip()
                st.success("✅ Logged in!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
else:
    st.success(f"🎉 Welcome, {st.session_state.app_username}!")
    st.write("You are logged in")


    if st.button("Log Out"): #log out
        st.session_state.app_username = None
        st.rerun()

