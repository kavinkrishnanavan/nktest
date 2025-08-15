import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from authlib.integrations.requests_client import OAuth2Session
import os

# 1️⃣ Copy secrets into a mutable dict
config = {
    "credentials": dict(st.secrets["credentials"]),
    "cookie": dict(st.secrets["cookie"]),
    "preauthorized": list(st.secrets["preauthorized"])
}

# 2️⃣ Streamlit Authenticator
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

# 3️⃣ Login form
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Welcome {name}")
    st.write("You have access to the app!")

elif authentication_status == False:
    st.error("Username/password is incorrect")

elif authentication_status == None:
    st.warning("Please enter your username and password")

# 4️⃣ Google OAuth Button
if st.button("Login with Google"):
    client_id = st.secrets["google"]["client_id"]
    client_secret = st.secrets["google"]["client_secret"]
    redirect_uri = st.secrets["google"]["redirect_uri"]
    
    scope = "openid email profile"
    oauth = OAuth2Session(client_id, client_secret, scope=scope, redirect_uri=redirect_uri)
    auth_url, state = oauth.create_authorization_url(
        "https://accounts.google.com/o/oauth2/auth"
    )
    st.markdown(f"[Click here to login with Google]({auth_url})")

# Handle callback in separate route
if "code" in st.query_params:
    code = st.query_params["code"]
    token = oauth.fetch_token(
        "https://oauth2.googleapis.com/token",
        authorization_response=st.request.url,
        code=code
    )
    user_info = oauth.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
    
    if user_info["email"] in st.secrets["allowed_emails"]:
        st.success(f"Welcome {user_info['name']} (Google)")
    else:
        st.error("Access denied — please contact the app owner.")
