import streamlit as st
import streamlit_authenticator as stauth
import bcrypt
import json
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import requests
import pathlib

# -------------------
# Load config from secrets
# -------------------
config = {
    "credentials": {
        "usernames": dict(st.secrets["credentials"]["usernames"])
    },
    "cookie": dict(st.secrets["cookie"]),
    "oauth": dict(st.secrets["oauth"])
}

# -------------------
# Setup Authenticator
# -------------------
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# -------------------
# Login form
# -------------------
st.title("🔐 My Web App Login")

name, authentication_status, username = authenticator.login("Login", location="main")

if authentication_status is False:
    st.error("Username or password is incorrect.")
elif authentication_status is None:
    st.warning("Please enter your username and password.")
elif authentication_status:
    st.success(f"Welcome {name}!")
    st.write("This is your main app content here.")
    authenticator.logout("Logout", "sidebar")

# -------------------
# Google OAuth Login
# -------------------
st.markdown("---")
st.subheader("Or Sign in with Google")

client_config = {
    "web": {
        "client_id": config["oauth"]["client_id"],
        "project_id": config["oauth"]["project_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": config["oauth"]["client_secret"],
        "redirect_uris": [config["oauth"]["redirect_uri"]],
        "javascript_origins": [config["oauth"]["javascript_origin"]]
    }
}

if st.button("Sign in with Google"):
    flow = Flow.from_client_config(
        client_config,
        scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
    )
    flow.redirect_uri = config["oauth"]["redirect_uri"]
    auth_url, _ = flow.authorization_url(prompt="consent")
    st.markdown(f"[Click here to authenticate]({auth_url})")

# After redirect, you’ll handle the Google response in your redirect URI endpoint
