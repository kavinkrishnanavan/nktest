import streamlit as st
import streamlit_authenticator as stauth
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import requests
import os

# --------------------------
# Load Config from secrets
# --------------------------
config = {
    "credentials": {
        "usernames": dict(st.secrets["credentials"]["usernames"])
    },
    "cookie": dict(st.secrets["cookie"]),
    "oauth": dict(st.secrets["oauth"])
}

# --------------------------
# Setup Authenticator
# --------------------------
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# --------------------------
# Login Form
# --------------------------
st.title("🔐 My Web App Login")

authentication_status = authenticator.login("Login", location="main")

# Google OAuth button
st.write("Or login with Google:")
if st.button("Sign in with Google"):
    client_secrets_file = "client_secrets.json"
    with open(client_secrets_file, "w") as f:
        f.write(f"""
{{
  "web": {{
    "client_id": "{config['oauth']['client_id']}",
    "project_id": "{config['oauth']['project_id']}",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "{config['oauth']['client_secret']}",
    "redirect_uris": ["{config['oauth']['redirect_uri']}"],
    "javascript_origins": ["{config['oauth']['redirect_uri']}"]
  }}
}}
""")
    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri=config['oauth']['redirect_uri']
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    st.write(f"[Click here to login with Google]({auth_url})")

# --------------------------
# Login State
# --------------------------
if authentication_status is False:
    st.error("Username or password is incorrect.")
elif authentication_status is None:
    st.warning("Please enter your username and password.")
elif authentication_status:
    st.success(f"Welcome {authenticator.get_name()}")
    st.write("✅ This is your main app content here.")
    authenticator.logout("Logout", "sidebar")
