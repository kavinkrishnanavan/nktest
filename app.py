import streamlit as st
import streamlit_authenticator as stauth
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import requests
import os
import json

st.set_page_config(page_title="My App with Google OAuth", layout="centered")

# --------------------------
# 1. COPY secrets into dicts so they are writable
# --------------------------
config = {
    "credentials": dict(st.secrets["credentials"]),
    "cookie": dict(st.secrets["cookie"]),
    "oauth": dict(st.secrets["oauth"])
}

# --------------------------
# 2. Setup Streamlit Authenticator for username/password login
# --------------------------
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# --------------------------
# 3. Login Form
# --------------------------
st.title("🔐 Welcome to My App")

login_option = st.radio("Choose login method:", ["Username & Password", "Google Login"])

if login_option == "Username & Password":
    name, auth_status, username = authenticator.login("Login", location="main")

    if auth_status:
        st.success(f"Welcome, {name}!")
        authenticator.logout("Logout", "sidebar")
        st.write("✅ You are now logged in.")
    elif auth_status is False:
        st.error("Username/password is incorrect")
    elif auth_status is None:
        st.warning("Please enter your username and password")

# --------------------------
# 4. Google OAuth Login
# --------------------------
elif login_option == "Google Login":
    client_id = config["oauth"]["client_id"]
    client_secret = config["oauth"]["client_secret"]
    redirect_uri = config["oauth"]["redirect_uri"]

    if "credentials" not in st.session_state:
        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            "?response_type=code"
            f"&client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            "&scope=openid%20email%20profile"
        )
        st.markdown(f"[Login with Google]({auth_url})")

    else:
        st.success("Logged in with Google!")
        st.write(st.session_state.credentials)

