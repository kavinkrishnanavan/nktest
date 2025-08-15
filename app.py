import streamlit as st
import streamlit_authenticator as stauth
import json
import os
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests

# ----------------------
# Load credentials from secrets.toml
# ----------------------
config = {
    "credentials": {
        "usernames": dict(st.secrets["credentials"]["usernames"])
    },
    "cookie": dict(st.secrets["cookie"]),
    "preauthorized": dict(st.secrets["preauthorized"]),
}

# ----------------------
# Streamlit Authenticator
# ----------------------
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

# ----------------------
# Google OAuth Setup
# ----------------------
GOOGLE_CLIENT_ID = st.secrets["google"]["client_id"]
GOOGLE_CLIENT_SECRET = st.secrets["google"]["client_secret"]
GOOGLE_REDIRECT_URI = st.secrets["google"]["redirect_uri"]
ALLOWED_EMAILS = st.secrets["allowed_emails"]

# This will be needed for local Google flow credentials.json
GOOGLE_CONFIG = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "project_id": "streamlit-oauth",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uris": [GOOGLE_REDIRECT_URI]
    }
}

# ----------------------
# Login Page
# ----------------------
st.title("🔐 Secure Login Page")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Login with Username & Password")
    name, authentication_status, username = authenticator.login("Login", "main")

with col2:
    st.subheader("Login with Google")
    auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        "?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&scope=openid%20email%20profile"
    )
    st.markdown(f"[Sign in with Google]({auth_url})")

# ----------------------
# Handle Google Callback
# ----------------------
if "code" in st.query_params:
    code = st.query_params["code"]

    flow = Flow.from_client_config(
        GOOGLE_CONFIG,
        scopes=["openid", "email", "profile"],
        redirect_uri=GOOGLE_REDIRECT_URI
    )

    flow.fetch_token(code=code)

    credentials = flow.credentials
    request_session = requests.Request()
    id_info = id_token.verify_oauth2_token(
        credentials.id_token, request_session, GOOGLE_CLIENT_ID
    )

    email = id_info.get("email")
    if email in ALLOWED_EMAILS:
        st.success(f"✅ Google Login Successful! Welcome {email}")
        st.session_state["authentication_status"] = True
        st.session_state["name"] = id_info.get("name")
        st.session_state["username"] = email
    else:
        st.error("❌ You are not authorized to access this app.")

# ----------------------
# If logged in, show content
# ----------------------
if st.session_state.get("authentication_status"):
    st.write(f"Welcome {st.session_state.get('name', '')}!")
    if st.button("Logout"):
        authenticator.logout("Logout", "main")
