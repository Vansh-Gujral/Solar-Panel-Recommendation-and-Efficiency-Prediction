# solar_dashboard/home.py
import streamlit as st
import importlib.util
import sys
from pathlib import Path

# Configure page (must be first Streamlit command)
st.set_page_config(
    page_title="Solar Analytics Hub",
    page_icon="☀️",
    layout="centered"
)

def load_module(module_name):
    """Dynamically import a module while preventing duplicate page config"""
    module_path = Path(__file__).parent / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    
    # Prevent duplicate set_page_config
    original_st_set_page_config = st.set_page_config
    def dummy_set_page_config(*args, **kwargs):
        pass
    st.set_page_config = dummy_set_page_config
    
    try:
        spec.loader.exec_module(module)
    finally:
        # Restore original function
        st.set_page_config = original_st_set_page_config
    
    return module

def show_recommendation():
    """Lazy-load the recommendation system"""
    try:
        recommendation = load_module("recommendation")
        if hasattr(recommendation, 'show_recommendation'):
            recommendation.show_recommendation()
        else:
            st.error("Recommendation module is missing required function")
    except Exception as e:
        st.error(f"Failed to load recommendation system: {str(e)}")
    st.button("← Back to Home", on_click=lambda: st.session_state.update({"nav": "home"}))

def show_prediction():
    """Lazy-load the prediction system"""
    try:
        predictor = load_module("efficiency_predictor")
        if hasattr(predictor, 'show_prediction'):
            predictor.show_prediction()
        else:
            st.error("Prediction module is missing required function")
    except Exception as e:
        st.error(f"Failed to load prediction system: {str(e)}")
    st.button("← Back to Home", on_click=lambda: st.session_state.update({"nav": "home"}))

# Navigation
def show_home():
    st.title("Solar Analytics Hub")
    st.markdown("""
    <style>
    .nav-button {
        height: 120px;
        border-radius: 10px;
        font-size: 18px;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        if st.button(
            "🔍 Panel Recommendation",
            key="rec",
            help="Find ideal solar panels for your needs",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.nav = "recommend"
    
    with col2:
        if st.button(
            "📈 Efficiency Analysis",
            key="pred",
            help="Predict your system's performance",
            use_container_width=True,
            type="secondary"
        ):
            st.session_state.nav = "predict"

    st.markdown("---")
    st.image("https://images.unsplash.com/photo-1508514177221-188b1cf16e9d?w=800", use_container_width=True)

# App router
if "nav" not in st.session_state:
    st.session_state.nav = "home"

if st.session_state.nav == "home":
    show_home()
elif st.session_state.nav == "recommend":
    show_recommendation()
elif st.session_state.nav == "predict":
    show_prediction()

