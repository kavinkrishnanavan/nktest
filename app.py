# app.py
import streamlit as st
import streamlit_authenticator as stauth
from typing import Optional

st.set_page_config(page_title="My App", page_icon="🔐", layout="centered")

# ===== Helpers =====
OWNER_EMAIL = st.secrets["auth"].get("owner_email")
ALLOWLIST = set(st.secrets["auth"].get("allowlist", []))


def gate_access(email: Optional[str] = None, username: Optional[str] = None) -> bool:
    """Allow entry only if email is in allowlist or is owner."""
    identifier = (email or username or "").strip().lower()
    if not identifier:
        st.error("We couldn't determine your identity. Please try again.")
        st.stop()
    if identifier in {e.lower() for e in ALLOWLIST} or (
        OWNER_EMAIL and identifier == OWNER_EMAIL.lower()
    ):
        return True
    # Not approved yet
    st.warning(
        f"You're signed in as **{identifier}**, but you don't have access yet.\n\n"
        "Please ask the owner to add your email to the app allowlist in "
        "Streamlit Cloud → Settings → Secrets."
    )
    st.stop()


def show_main_app(name: str, email: Optional[str]):
    st.success(f"Access granted. Welcome, {name}!")
    st.write("Your email:", email)
    st.divider()
    # TODO: Put your real app content below
    st.write("This is your protected app area.")


# ===== UI =====
st.title("🔐 Welcome")
st.caption("Log in with Google or with a local account.")

tab_google, tab_password = st.tabs(["Continue with Google", "Email & Password"])

# --- Google tab (built-in Streamlit OAuth) ---
with tab_google:
    if not getattr(st, "user", None) or not getattr(st.user, "is_logged_in", False):
        st.button("Continue with Google", on_click=st.login, use_container_width=True)
        st.caption("We'll ask Google to verify your identity.")
    else:
        email = getattr(st.user, "email", None)
        name = getattr(st.user, "name", "User")
        if gate_access(email=email):
            st.button("Log out", on_click=st.logout)
            show_main_app(name=name, email=email)

# --- Email & Password tab (streamlit-authenticator) ---
with tab_password:
    config = st.secrets["auth_users"]
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    auth_status = st.session_state.get("authentication_status")
    if auth_status:
        username = st.session_state.get("username")
        name = st.session_state.get("name", username)
        # Lookup the user's email from the config
        email = (
            config["credentials"]["usernames"].get(username, {}).get("email")
        )
        if gate_access(email=email, username=username):
            authenticator.logout("Log out", "main")
            show_main_app(name=name, email=email)
    elif auth_status is False:
        st.error("Username/password is incorrect")
    else:
        st.info("Enter your username and password to log in.")# app.py
import streamlit as st
import streamlit_authenticator as stauth
from typing import Optional

st.set_page_config(page_title="My App", page_icon="🔐", layout="centered")

# ===== Helpers =====
OWNER_EMAIL = st.secrets["auth"].get("owner_email")
ALLOWLIST = set(st.secrets["auth"].get("allowlist", []))


def gate_access(email: Optional[str] = None, username: Optional[str] = None) -> bool:
    """Allow entry only if email is in allowlist or is owner."""
    identifier = (email or username or "").strip().lower()
    if not identifier:
        st.error("We couldn't determine your identity. Please try again.")
        st.stop()
    if identifier in {e.lower() for e in ALLOWLIST} or (
        OWNER_EMAIL and identifier == OWNER_EMAIL.lower()
    ):
        return True
    # Not approved yet
    st.warning(
        f"You're signed in as **{identifier}**, but you don't have access yet.\n\n"
        "Please ask the owner to add your email to the app allowlist in "
        "Streamlit Cloud → Settings → Secrets."
    )
    st.stop()


def show_main_app(name: str, email: Optional[str]):
    st.success(f"Access granted. Welcome, {name}!")
    st.write("Your email:", email)
    st.divider()
    # TODO: Put your real app content below
    st.write("This is your protected app area.")


# ===== UI =====
st.title("🔐 Welcome")
st.caption("Log in with Google or with a local account.")

tab_google, tab_password = st.tabs(["Continue with Google", "Email & Password"])

# --- Google tab (built-in Streamlit OAuth) ---
with tab_google:
    if not getattr(st, "user", None) or not getattr(st.user, "is_logged_in", False):
        st.button("Continue with Google", on_click=st.login, use_container_width=True)
        st.caption("We'll ask Google to verify your identity.")
    else:
        email = getattr(st.user, "email", None)
        name = getattr(st.user, "name", "User")
        if gate_access(email=email):
            st.button("Log out", on_click=st.logout)
            show_main_app(name=name, email=email)

# --- Email & Password tab (streamlit-authenticator) ---
with tab_password:
    config = st.secrets["auth_users"]
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    auth_status = st.session_state.get("authentication_status")
    if auth_status:
        username = st.session_state.get("username")
        name = st.session_state.get("name", username)
        # Lookup the user's email from the config
        email = (
            config["credentials"]["usernames"].get(username, {}).get("email")
        )
        if gate_access(email=email, username=username):
            authenticator.logout("Log out", "main")
            show_main_app(name=name, email=email)
    elif auth_status is False:
        st.error("Username/password is incorrect")
    else:
        st.info("Enter your username and password to log in.")
