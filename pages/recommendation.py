import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image
import smtplib
from email.message import EmailMessage
from twilio.rest import Client

TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = st.secrets["TWILIO_PHONE_NUMBER"]

SMTP_SERVER = st.secrets["SMTP_SERVER"]
SMTP_PORT = st.secrets["SMTP_PORT"]
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
SENDER_PASSWORD = st.secrets["SENDER_PASSWORD"]


# Cache dataset generation to improve performance
@st.cache_data
def generate_solar_panel_data():
    np.random.seed(42)
    companies = ["Tata Power", "Luminous", "Adani Solar", "Vikram Solar", "Waaree"]
    panel_types = ["Monocrystalline", "Polycrystalline", "Thin-film"]
    climates = ["Hot", "Sunny", "Temperate", "Cloudy"]

    data = {
        "Company": np.random.choice(companies, 20000),
        "Panel_Type": np.random.choice(panel_types, 20000, p=[0.4, 0.4, 0.2]),
        "Efficiency (%)": np.random.uniform(14, 22, 20000),
        "Power_Output (W)": np.random.randint(250, 500, 20000),
        "Lifespan (years)": np.random.randint(20, 30, 20000),
        "Warranty (years)": np.random.randint(10, 25, 20000),
        "Cost (₹)": np.random.randint(10000, 50000, 20000),
        "Best_Climate": np.random.choice(climates, 20000)
    }

    return pd.DataFrame(data)

# Function to determine panel type based on budget
def get_panel_category(budget):
    if budget < 20000:
        return "Thin-film"
    elif 20000 <= budget < 35000:
        return "Polycrystalline"
    else:
        return "Monocrystalline"

# Function to handle booking
def select_panel(company, panel_type):
    st.session_state.selected_panel = panel_type
    st.session_state.selected_company = company
    st.session_state.show_payment = True

# Function to send email
def send_email(to_email, name, panel_name, company_name):
    msg = EmailMessage()
    msg["Subject"] = "Solar Panel Booking Confirmation"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    msg.set_content(f"""
    Hello {name},

    Thank you for booking a {panel_name} solar panel from {company_name}.

    Your request has been received, and our team will contact you soon.

    Regards,
    Solar Panel Team
    """)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"⚠️ Error sending email: {e}")

# Function to make an AI-powered confirmation call
def make_call(to_phone, name, panel_name, company_name):
    client = Client(st.secrets["TWILIO_ACCOUNT_SID"], st.secrets["TWILIO_AUTH_TOKEN"])
    
    message = f"Hello {name}, thank you for booking a {panel_name} solar panel from {company_name}. Our team will contact you soon."
    try:
        call = client.calls.create(
            twiml=f'<Response><Say voice="alice">{message}</Say></Response>',
            to=to_phone,
            from_=st.secrets["TWILIO_PHONE_NUMBER"]
        )
        st.success("📞 Call initiated successfully!")
        print(call.sid)  # Optional: useful for debugging/logging
    except Exception as e:
        st.error(f"⚠️ Error making call: {e}")
        print("Twilio Call Error:", e)


# Function to save booking details & trigger email & call
def save_booking(name, phone, email, panel_name, company_name):
    booking_data = f"Name: {name}, Phone: {phone}, Email: {email}, Panel: {panel_name}, Company: {company_name}\n"
    
    with open("booking.txt", "a") as f:
        f.write(booking_data)
    
    send_email(email, name, panel_name, company_name)
    make_call(phone, name, panel_name, company_name)

# Function to display payment gateway
def show_payment_gateway(panel_name, company_name):
    """Displays payment options with customer information form"""
    st.markdown("---")
    st.subheader(f"Book {panel_name} from {company_name}")
    
    payment_image_path = "payment.jpg"
    if os.path.exists(payment_image_path):
        payment_qr = Image.open(payment_image_path)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(payment_qr, caption="Scan QR to Pay", width=200)
    with col2:
        st.markdown("""
        **Payment Details:**
        - UPI ID: vanshgujral175@oksbi
        - Amount: ₹500 (Booking fee)
        - Note: Include your email in the payment note
        """)

    st.markdown("### Enter Your Details to Complete Booking")
    with st.form(key="booking_form"):
        name = st.text_input("Full Name*", placeholder="John Doe")
        phone = st.text_input("Phone Number*", placeholder="9876543210")
        email = st.text_input("Email*", placeholder="example@gmail.com")

        submitted = st.form_submit_button("Submit Booking Request")
        if submitted:
            if not all([name, phone, email]):
                st.error("Please fill all required fields (*)")
            else:
                save_booking(name, phone, email, panel_name, company_name)
                st.success(f"Booking request received! We'll contact {name} shortly.")
                st.balloons()
                st.session_state.show_payment = False

    if st.button("← Back to Recommendations"):
        st.session_state.show_payment = False

# Function to display data analysis
def show_data_analysis(df):
    with st.expander("📊 **Data Analysis Tool**"):
        st.markdown("### Dataset Sample:")
        st.dataframe(df.head(10))

        st.markdown("### Dataset Statistics:")
        st.write(df.describe())

        # Cost vs Efficiency Scatter Plot
        st.markdown("### 💰 Cost vs Efficiency")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x="Cost (₹)", y="Efficiency (%)", hue="Panel_Type", palette="coolwarm", ax=ax)
        st.pyplot(fig)
# Main function
def show_recommendation():
    st.title("🌞 Solar Panel Recommendation System")

    if 'show_payment' not in st.session_state:
        st.session_state.show_payment = False

    df = generate_solar_panel_data()

    col1, col2 = st.columns(2)
    with col1:
        budget = st.slider("Your Budget (₹):", 10000, 50000, 25000, step=1000)
    with col2:
        climate = st.selectbox("Your Primary Climate:", ["Hot", "Sunny", "Temperate", "Cloudy"])

    preferred_type = get_panel_category(budget)  # Determine panel type based on budget

    if st.button("Get Recommendations"):
        suitable_panels = df[(df["Cost (₹)"] <= budget) & 
                             (df["Best_Climate"] == climate) & 
                             (df["Panel_Type"] == preferred_type)]

        if suitable_panels.empty:
            suitable_panels = df[(df["Cost (₹)"] <= budget) & (df["Panel_Type"] == preferred_type)]

        if suitable_panels.empty:
            suitable_panels = df[df["Cost (₹)"] <= budget]

        st.session_state.recommendations = suitable_panels.sort_values("Efficiency (%)", ascending=False).head(3)
        st.session_state.show_payment = False

    if st.session_state.show_payment:
        show_payment_gateway(
            st.session_state.selected_panel,
            st.session_state.selected_company
        )
    elif 'recommendations' in st.session_state and not st.session_state.recommendations.empty:
        st.markdown("### 🔥 Top Recommendations:")

        # Ensure recommendations are displayed horizontally
        cols = st.columns(len(st.session_state.recommendations))

        for idx, (_, row) in enumerate(st.session_state.recommendations.iterrows()):
            with cols[idx]:
                st.markdown(f"""
                **{row['Company']} - {row['Panel_Type']}**  
                💰 **Cost:** ₹{row['Cost (₹)']}  
                ⚡ **Efficiency:** {row['Efficiency (%)']:.1f}%  
                🔋 **Power:** {row['Power_Output (W)']}W  
                ⏳ **Lifespan:** {row['Lifespan (years)']} years  
                🛠 **Warranty:** {row['Warranty (years)']} years  
                🌤 **Best Climate:** {row['Best_Climate']}  
                """)
                if st.button(f"Book {row['Company']}", key=f"{row['Company']}_{idx}"):
                    select_panel(row['Company'], row['Panel_Type'])

    # Data Analysis Section inside a dropdown (expander)
    show_data_analysis(df)

# Run the app
if __name__ == "__main__":
    show_recommendation()
