import streamlit as st
from utils.auth import hash_password
from sqlalchemy import text


if "app_username" not in st.session_state:
    st.session_state.app_username = None

if st.session_state.app_username:
    st.write("You are already logged in!")

else:
    with st.form("signup_form"):
        new_user = st.text_input("Choose a username")
        new_pass = st.text_input("Choose a password", type="password")
        submit = st.form_submit_button("Create Account")

        if submit and new_user and new_pass:
            hashed = hash_password(new_pass)
            conn = st.connection("postgresql", type="sql")
            try:
                with conn.session as session:
                    session.execute(
                        text(
                            "INSERT INTO Users (app_username, app_password) "
                            "VALUES (:username, :password)"
                        ),
                        params = {"username": new_user.strip(), "password": hashed},
                    )
                    session.commit()

                st.success("✅ Account created! You can now log in.")
            except Exception as e:
                st.error(f"An error occurred: {e}")