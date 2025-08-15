import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from google_auth_oauthlib.flow import Flow
import os
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# --------------------------
# LOAD CONFIG FROM SECRETS
# --------------------------
config = {
    "credentials": st.secrets["credentials"],
    "cookie": st.secrets["cookie"]
}

# --------------------------
# STREAMLIT AUTHENTICATOR LOGIN
# --------------------------
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# --------------------------
# LOGIN FORM
# --------------------------
st.title("My Secure App")

# Standard username/password login
name, authentication_status, username = authenticator.login("Login", "main")

# Google OAuth Login Button
if st.button("Sign in with Google"):
    client_id = st.secrets["google"]["client_id"]
    client_secret = st.secrets["google"]["client_secret"]
    redirect_uri = st.secrets["google"]["redirect_uri"]

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": [redirect_uri],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"]
    )
    flow.redirect_uri = redirect_uri

    auth_url, _ = flow.authorization_url(prompt='consent')
    st.markdown(f"[Click here to sign in with Google]({auth_url})")

# --------------------------
# POST-LOGIN BEHAVIOR
# --------------------------
if authentication_status:
    st.success(f"Welcome {name}!")
    st.write("You can now access the app.")
    authenticator.logout("Logout", "sidebar")

elif authentication_status is False:
    st.error("Username/password is incorrect")

elif authentication_status is None:
    st.warning("Please enter your username and password")
