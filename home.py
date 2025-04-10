import streamlit as st
import numpy as np
import pandas as pd
import random
import importlib.util
import sys
from pathlib import Path

# Ensure page config is set only once
if "page_config_set" not in st.session_state:
    st.set_page_config(page_title="Solar Panel Selection", layout="wide")
    st.session_state["page_config_set"] = True

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)


def calculate_savings(monthly_bill):
    """Estimates savings based on electricity bill."""
    savings = monthly_bill * 0.6  # Assuming 60% savings
    return max(savings, 0)

def show_home_page():
    # Title and Description
    st.markdown("""
    <h1 style='text-align: center;'>☀️ Solar Panel Selection & Efficiency Prediction</h1>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        st.write("""
        Welcome to our AI-powered solar panel recommendation and efficiency prediction system. Save energy, reduce costs, and make informed solar choices!
        
        ## About the Project
        Solar energy is one of the most sustainable ways to reduce electricity bills and contribute to a greener planet. Our system helps you:
        - **Find the best solar panel** based on your budget, efficiency, and climate conditions.
        - **Predict the efficiency** of an installed solar panel based on real-time factors.
        - **Estimate your potential savings** when switching to solar energy.
        - **Make data-driven decisions** for long-term sustainability and cost-effectiveness.
        """)

    with col2:
        st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdXVoOWRiMG50eW1zY3p0aXlhbWhnNXAybXBwNDlqNndvY282NG96cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dOrKc4pASvkZfdu5uz/giphy.gif", width=450)
    
    st.markdown("---")
    
    # Solar Savings Calculator
    st.subheader("💰 Solar Savings Calculator")
    monthly_bill = st.number_input("Enter Your Monthly Electricity Bill (₹):", min_value=500, max_value=20000, value=5000, step=500)
    
    if st.button("Estimate Savings", use_container_width=True):
        savings = calculate_savings(monthly_bill)
        st.success(f"🌞 Estimated Monthly Savings: ₹{savings:.2f}")
    
    st.markdown("---")
    
    # Random Solar Energy Fact
    solar_facts = [
        "Solar energy is the most abundant energy source on Earth.",
        "A solar panel system can reduce electricity bills by up to 80%.",
        "The largest solar power plant is in the Mojave Desert, USA.",
        "Monocrystalline panels have the highest efficiency.",
        "Solar panels can last more than 25 years with proper maintenance."
    ]
    st.info(f"🔆 Did you know? {random.choice(solar_facts)}")
    
    st.markdown("---")

    # Buttons for Recommendations & Efficiency Prediction
    col1, col2, col3 = st.columns(3, gap="large")

    if col1.button(
        "🔍 Panel Recommendation",
        key="rec",
        help="Find ideal solar panels for your needs",
        use_container_width=True,
        type="primary"
    ):
        st.session_state["nav"] = "recommend"
        st.rerun()

    if col2.button(
        "📈 Efficiency Analysis",
        key="pred",
        help="Predict your system's performance",
        use_container_width=True,
        type="secondary"
    ):
        st.session_state["nav"] = "predict"
        st.rerun()

    if col3.button(
    "💰 Subsidy Info",
    key="subsidy",
    help="Check government subsidy eligibility",
    use_container_width=True,
    type="secondary"
    ):
        st.session_state["nav"] = "subsidy"
        st.rerun()
    

    st.markdown("---")


def load_module(module_name):
    """Dynamically import a module while preventing duplicate page config"""
    module_path = Path(__file__).parent / f"pages/{module_name}.py"
    if not module_path.exists():
        st.error(f"Error: {module_name}.py not found in the 'pages' directory.")
        return None
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module  # Register module in sys.modules
    
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"Failed to load {module_name}: {str(e)}")
        return None

    
def show_recommendation():
    """Lazy-load the recommendation system"""
    recommendation = load_module("recommendation")
    if recommendation and hasattr(recommendation, 'show_recommendation'):
        recommendation.show_recommendation()
    else:
        st.error("Recommendation module is missing required function.")

    if st.button("← Back to Home", key="back_home_1"):
        st.session_state["nav"] = "home"
        st.rerun()


def show_prediction():
    """Lazy-load the prediction system"""
    predictor = load_module("efficiency_predictor")
    if predictor and hasattr(predictor, 'show_prediction'):
        predictor.show_prediction()
    else:
        st.error("Prediction module is missing required function.")

    if st.button("← Back to Home", key="back_home_2"):
        st.session_state["nav"] = "home"
        st.rerun()


def show_subsidy():
    """Lazy-load the subsidy info page"""
    subsidy = load_module("subsidy")
    if subsidy and hasattr(subsidy, 'show_subsidy'):
        subsidy.show_subsidy()
    else:
        st.error("Subsidy module is missing required function.")

    if st.button("← Back to Home", key="back_home_3"):
        st.session_state["nav"] = "home"
        st.rerun()

# Ensure session state for navigation
if "nav" not in st.session_state:
    st.session_state["nav"] = "home"

# App Router
if st.session_state["nav"] == "home":
    show_home_page()
elif st.session_state["nav"] == "recommend":
    show_recommendation()
elif st.session_state["nav"] == "predict":
    show_prediction()
elif st.session_state["nav"] == "subsidy":
    from pages import subsidy
    subsidy.show_subsidy_page()
