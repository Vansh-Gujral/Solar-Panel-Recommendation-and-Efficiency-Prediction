import streamlit as st
from streamlit_lottie import st_lottie
import requests

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------
st.set_page_config(
    page_title="Solar Efficiency App",
    layout="wide",
    initial_sidebar_state="collapsed"  # 👈 This hides the sidebar by default
)

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



def calculate_savings(electricity_rate, daily_consumption, sunlight_hours, panel_capacity):
    output_per_day = panel_capacity * sunlight_hours  # kWh/day
    daily_savings = min(daily_consumption, output_per_day) * electricity_rate
    monthly_savings = daily_savings * 30
    yearly_savings = monthly_savings * 12
    return output_per_day, daily_savings, monthly_savings, yearly_savings

# -----------------------------
# PAGE CONFIG & STYLING
# -----------------------------

st.set_page_config(page_title="Solar Smart AI", page_icon="🌞", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f0f9ff;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton > button {
        background-color: #026773;
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 10px;
    }
    .stButton > button:hover {
        background-color: #014d56;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER + HERO SECTION
# -----------------------------

solar_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_i2eyukor.json")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<h1 style='font-size: 50px; color: #034d5e;'>Welcome to Solar Smart AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px;'>Empowering your home with solar intelligence. Estimate your savings, get the best panel recommendations, and check subsidies instantly.</p>", unsafe_allow_html=True)
with col2:
    st_lottie(solar_animation, height=300, key="solar-anim")

# -----------------------------
# NAVIGATION BUTTONS
# -----------------------------

st.markdown("##")
nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("🔍 Solar Recommendation"):
        st.switch_page("pages/recommendation.py")
with nav2:
    if st.button("⚙️ Efficiency Predictor"):
        st.switch_page("pages/efficiency_predictor.py")
with nav3:
    if st.button("🏛️ Subsidy Info"):
        st.switch_page("pages/subsidy.py")

# -----------------------------
# SOLAR SAVINGS CALCULATOR
# -----------------------------

st.markdown("---")
st.markdown("<h2 style='color: #025464;'>💰 Solar Savings Calculator</h2>", unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2)

    with c1:
        electricity_rate = st.number_input("Electricity Rate (₹/kWh)", min_value=1.0, max_value=20.0, value=8.0, step=0.5)
        daily_consumption = st.number_input("Daily Electricity Consumption (kWh)", min_value=1.0, max_value=100.0, value=10.0, step=1.0)

    with c2:
        sunlight_hours = st.number_input("Avg Sunlight Hours/Day", min_value=1.0, max_value=12.0, value=5.0, step=0.5)
        panel_capacity = st.number_input("Solar Panel Capacity (kW)", min_value=0.5, max_value=20.0, value=3.0, step=0.5)

    if st.button("⚡ Estimate Savings", use_container_width=True):
        output, daily, monthly, yearly = calculate_savings(
            electricity_rate, daily_consumption, sunlight_hours, panel_capacity
        )
        st.success(f"🌞 Monthly Savings: ₹{monthly:,.2f}")
        st.info(f"📅 Yearly Savings: ₹{yearly:,.2f}")
        st.write(f"🔋 Daily Solar Output: {output:.2f} kWh")
        st.write(f"💸 Daily Savings: ₹{daily:.2f}")

# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>Crafted with love for a greener tomorrow | © 2025 Solar Smart AI</p>", unsafe_allow_html=True)
