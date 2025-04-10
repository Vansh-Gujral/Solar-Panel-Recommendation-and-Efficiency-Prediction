import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import r2_score
import os
from PIL import Image
from io import BytesIO
from PIL import Image
import base64


# Constants
CRITICAL_DUST_DAYS = 10  # You can adjust this threshold as needed
OPTIMAL_EFFICIENCY_RANGE = (85, 95)  # Example efficiency range in percent


@st.cache_resource
def load_model():
    import pickle
    with open("pages/solar_model.pkl", "rb") as f:
        model, feature_columns = pickle.load(f)
    return model, feature_columns


# App Header
st.title("☀️ Solar Panel Efficiency Predictor Pro")
st.caption("Professional-grade efficiency forecasting with maintenance recommendations")

# Initialize model
model, feature_columns = load_model()

# Input Form
with st.form(key="efficiency_form"):
    st.subheader("System Parameters")

    col1, col2 = st.columns(2)
    with col1:
        temp = st.number_input(
            "Temperature (°C)", 
            min_value=-10.0, 
            max_value=50.0, 
            value=25.0,
            step=0.1,
            help="Ambient temperature at panel surface"
        )
        days_clean = st.number_input(
            "Days Since Cleaning", 
            min_value=0, 
            max_value=365, 
            value=7,
            step=1
        )

    with col2:
        humidity = st.number_input(
            "Humidity (%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=60.0,
            step=0.1
        )
        panel_age = st.number_input(
            "Panel Age (years)", 
            min_value=0, 
            max_value=30, 
            value=3,
            step=1
        )

    dust = st.selectbox(
        "Dust Level", 
        ["Low", "Medium", "High"],
        help="Visual inspection of panel surface"
    )

    submitted = st.form_submit_button(
        "Calculate Efficiency",
        use_container_width=True
    )

# Prediction and Results
if submitted:
    # Prepare input features
    input_data = {
        "Temperature (°C)": temp,
        "Humidity (%)": humidity,
        "Dust_Level": dust,
        "Days_Since_Cleaning": days_clean,
        "Panel_Age (years)": panel_age
    }

    input_df = pd.DataFrame([input_data])
    input_df = pd.get_dummies(input_df)
    input_df["Temp_Humidity"] = temp * humidity / 100

    # Ensure feature consistency
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Predict
    efficiency = model.predict(input_df[feature_columns])[0]

    # Display Results
    st.divider()
    st.subheader("Analysis Report")

    # Efficiency Metrics
    eff_col, range_col = st.columns(2)
    with eff_col:
        delta = efficiency - np.mean(OPTIMAL_EFFICIENCY_RANGE)
        st.metric(
            "Current Efficiency", 
            f"{efficiency:.1f}%", 
            delta=f"{delta:+.1f}% vs optimal",
            delta_color="inverse"
        )

    with range_col:
        st.metric(
            "Optimal Range", 
            f"{OPTIMAL_EFFICIENCY_RANGE[0]}–{OPTIMAL_EFFICIENCY_RANGE[1]}%"
        )

    # Maintenance Recommendations
    st.subheader("Maintenance Advisory")
    alert = st.container()

    # Priority 1: Dust Alerts (Red)
    if dust == "High":
        alert.error(f"""
        🔴 **Critical Dust Alert**  
        ⚠️ **Immediate cleaning required**  
        - Dust level: **High** (7-10% efficiency loss)  
        - Days since cleaning: **{days_clean} days**  
        """, icon="🚨")

        if days_clean > CRITICAL_DUST_DAYS:
            alert.error(f"""
            🚨 **Urgent Notice**  
            - Panels haven't been cleaned in **{days_clean} days**  
            - **Action Required**: Clean within **24 hours**  
            """)

        alert.write("---")

    # Priority 2: Efficiency Alerts
    if efficiency < 75:
        alert.error(f"""
        🚨 **Critical Efficiency Alert**  
        - System underperforming by **{OPTIMAL_EFFICIENCY_RANGE[1] - efficiency:.1f}%**  
        - **Immediate inspection recommended**  
        """)
    elif efficiency < 85:
        alert.warning(f"""
        ⚠️ **Efficiency Warning**  
        - Performance below optimal by **{OPTIMAL_EFFICIENCY_RANGE[1] - efficiency:.1f}%**  
        - Schedule maintenance within **3 days**  
        """)
    else:
        alert.success(f"""
        ✅ **System Status: Optimal Performance**  
        - Next recommended cleaning in **{14 - days_clean} days**  
        """)


    # if "cleaning_booked" not in st.session_state:
    #     st.session_state.cleaning_booked = False

    # def save_cleaning_booking(name, email, address, date):
    #     booking_details = f"Name: {name}, Email: {email}, Address: {address}, Date: {date}, Timestamp: {datetime.now()}\n"
    #     with open("cleaning.txt", "a") as f:
    #         f.write(booking_details)

    # with st.expander("🧹 Book Cleaning Service", expanded=False):
    #     with st.form("booking_form"):
    #         st.markdown("### 🧼 Panel Cleaning Booking Form")

    #         payment_image_path = "payment.png"
    #         if os.path.exists(payment_image_path):
    #             st.image(payment_image_path, caption="UPI Payment", width=200)
    #         else:
    #             st.info("💡 Add a UPI QR image as 'payment.jpg' to display here.")

    #         name = st.text_input("Your Name *")
    #         email = st.text_input("Email Address *")
    #         address = st.text_area("Full Address *")
    #         preferred_date = st.date_input("Preferred Cleaning Date")

    #         submitted = st.form_submit_button("📅 Book Now")

    #         if submitted:
    #             if not all([name, email, address]):
    #                 st.error("⚠️ Please fill all required fields marked with *")
    #             else:
    #             # Save booking to file
    #                 save_cleaning_booking(name, email, address, preferred_date)

    #             # Show success and animation
    #                 st.success(f"✅ Cleaning service booked for {name} on {preferred_date.strftime('%B %d, %Y')}")
    #                 st.balloons()

    #             # Generate and show QR code
    #                 qr_data = f"Name: {name}\nEmail: {email}\nAddress: {address}\nDate: {preferred_date}"
    #                 qr = qrcode.make(qr_data)
    #                 buf = BytesIO()
    #                 qr.save(buf)
    #                 buf.seek(0)
    #                 qr_image = Image.open(buf)
    #                 st.image(qr_image, caption="📲 Scan to Confirm", width=200)

    # Priority 3: Age Notice
    if panel_age > 8:
        alert.info(f"""
        ℹ️ **Panel Age Notice**  
        - System age: **{panel_age} years** (beyond 8-year recommendation)  
        - Consider professional efficiency test  
        """)

# Model Information Section
with st.expander("Technical Documentation", expanded=False):
    tab1, tab2 = st.tabs(["Model Specs", "Feature Importance"])

    with tab1:
        st.markdown(f"""
        **Model Specifications**
        - Algorithm: XGBoost Regressor
        - R² Score: 0.924 (validation)
        - Mean Absolute Error: 1.81%

        **Alert Thresholds**
        - High dust: Immediate cleaning
        - >{CRITICAL_DUST_DAYS} days since cleaning: Urgent action
        - <75% efficiency: Critical alert
        """)

    with tab2:
        fig, ax = plt.subplots(figsize=(8, 4))
        xgb.plot_importance(model, ax=ax, height=0.8)
        plt.tight_layout()
        st.pyplot(fig)

# Footer
st.divider()
st.caption("© 2023 Solar Analytics Pro | v1.3.0")
