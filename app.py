import streamlit as st
import requests
import webbrowser
import os

CLIENT_ID = "991628707019-q09r1u88vb610e8f3g3jnvcf3eabvdb8.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8501"

AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

st.set_page_config(page_title="Login", page_icon="🔐")
st.title("☀️ Solar Panel Selection & Efficiency Prediction ☀️")
st.subheader("Login to Continue")

# Forcefully hide Streamlit's default sidebar
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)


# 🚨 Replace with your actual Google OAuth credentials

# 🔹 Generate Google Login URL
login_url = (
    f"{AUTHORIZATION_URL}?response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope=openid%20email%20profile"
    f"&access_type=offline"
    f"&prompt=consent"
)

# 🔹 Login Button (Opens Google OAuth Page)
if st.button("Login with Google"):
    webbrowser.open(login_url)

# 🔹 Handle OAuth Callback
if "code" in st.query_params and "user_info" not in st.session_state:
    try:
        # Exchange Code for Access Token
        token_response = requests.post(
            TOKEN_URL,
            data={
                "code": st.query_params["code"],
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        ).json()

        # ✅ If access token received, get user info
        if "access_token" in token_response:
            user_info = requests.get(USER_INFO_URL, headers={"Authorization": f"Bearer {token_response['access_token']}"}).json()
            st.session_state["user_info"] = user_info
            st.success(f"Welcome, {user_info['name']}! 🎉")

            # ✅ Open `home.py` after login
            st.query_params["user"] = "Vansh"
            os.system("streamlit run home.py")

        else:
            st.error("Login failed. Please try again.")
            st.json(token_response)  # Show error response for debugging

    except Exception as e:
        st.error(f"Login Error: {str(e)}")

# 🔹 If Already Logged In, Open `home.py`
if "user_info" in st.session_state:
    st.success(f"Welcome back, {st.session_state['user_info']['name']}! 🎉")
    os.system("streamlit run home.py")
