import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import pickle
import matplotlib.pyplot as plt

def select_panel(company, panel_type):
    """Stores selected panel details and triggers the payment gateway"""
    st.session_state.selected_panel = panel_type
    st.session_state.selected_company = company
    st.session_state.show_payment = True

def save_booking(name, phone, email, panel_name, company_name):
    """Saves the booking details to a .txt file"""
    
    booking_data = f"Name: {name}, Phone: {phone}, Email: {email}, Panel: {panel_name}, Company: {company_name}\n"
    
    # Append to booking.txt file
    with open("booking.txt", "a") as f:
        f.write(booking_data)

def show_payment_gateway(panel_name, company_name):
    """Displays payment options with customer information form"""
    st.markdown("---")
    st.subheader(f"Book {panel_name} from {company_name}")
    
    with st.form("customer_info"):
        st.write("**Please fill your details:**")
        name = st.text_input("Full Name*")
        phone = st.text_input("Phone Number*")
        email = st.text_input("Email*")
        upi_id = st.text_input("UPI Transaction ID (after payment)")
        
        st.markdown("### Payment Method")
        try:
            qr_code = Image.open("payment.png")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(qr_code, caption="Scan QR to Pay", width=200)
            with col2:
                st.markdown("""
                **Payment Details:**
                - UPI ID: `8077439345@ybl`
                - Amount: ₹500 (Booking fee)
                - Note: Include your email in payment note
                """)
        except:
            st.warning("Payment QR code not found")
        
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


def generate_solar_panel_data():
    """Generates synthetic solar panel data with company information"""
    panel_types = ["Monocrystalline", "Polycrystalline", "Thin-film"]
    companies = {
        "Monocrystalline": ["SunPower", "LG", "Panasonic"],
        "Polycrystalline": ["Canadian Solar", "Jinko Solar", "Trina Solar"],
        "Thin-film": ["First Solar", "Solar Frontier", "Hanergy"]
    }
    
    n_samples = 500
    data = {
        "Panel_Type": np.random.choice(panel_types, n_samples),
        "Company": [np.random.choice(companies[pt]) for pt in np.random.choice(panel_types, n_samples)],
        "Cost (₹)": np.random.randint(10000, 25000, n_samples),
        "Power_Output (W)": np.random.choice([300, 350, 400, 450], n_samples),
        "Best_Climate": np.random.choice(["Hot", "Sunny", "Temperate", "Cloudy"], n_samples)
    }
    
    efficiency_ranges = {
        "Monocrystalline": (20, 22),
        "Polycrystalline": (16, 18),
        "Thin-film": (15, 17)
    }
    lifespan_ranges = {
        "Monocrystalline": (25, 30),
        "Polycrystalline": (20, 25),
        "Thin-film": (15, 20)
    }
    warranty_ranges = {
        "Monocrystalline": (20, 25),
        "Polycrystalline": (15, 20),
        "Thin-film": (10, 15)
    }
    
    data["Efficiency (%)"] = [np.random.uniform(*efficiency_ranges[panel]) for panel in data["Panel_Type"]]
    data["Lifespan (years)"] = [np.random.randint(*lifespan_ranges[panel]) for panel in data["Panel_Type"]]
    data["Warranty (years)"] = [np.random.randint(*warranty_ranges[panel]) for panel in data["Panel_Type"]]
    
    df = pd.DataFrame(data)
    df.to_csv("solar_panel_data.csv", index=False)  # Save dataset to CSV
    return df

def show_recommendation():
    """Main recommendation interface"""
    st.title("🌞 Solar Panel Recommendation System")
    
    if 'show_payment' not in st.session_state:
        st.session_state.show_payment = False
    
    col1, col2 = st.columns(2)
    with col1:
        budget = st.slider("Your Budget (₹):", 10000, 50000, 25000, step=1000)
    with col2:
        climate = st.selectbox("Your Primary Climate:", 
                             ["Hot", "Sunny", "Temperate", "Cloudy"])
    
    df = generate_solar_panel_data()
    
    if st.button("Get Recommendations"):
        st.session_state.recommendations = df[df["Cost (₹)"] <= budget].sort_values("Efficiency (%)", ascending=False).head(3)
        st.session_state.show_payment = False
    
    if st.session_state.show_payment:
        show_payment_gateway(
            st.session_state.selected_panel,
            st.session_state.selected_company
        )
    elif 'recommendations' in st.session_state:
        st.markdown("### Top Recommendations:")
        
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
                """)
                if st.button(f"Book {row['Company']}", key=f"{row['Company']}_{idx}"):
                    select_panel(row['Company'], row['Panel_Type'])
    
    st.markdown("---")
    with st.expander("📊 Data Analysis Tools"):
        tab1, tab2 = st.tabs(["Raw Data", "Visualizations"])
        
        with tab1:
            st.dataframe(df.sort_values("Efficiency (%)", ascending=False))
        
        with tab2:
            st.subheader("Cost vs Efficiency Analysis")
            fig, ax = plt.subplots(figsize=(8, 4))
            
            colors = {
                "Monocrystalline": "red",
                "Polycrystalline": "blue", 
                "Thin-film": "green"
            }
            
            for panel_type, group in df.groupby("Panel_Type"):
                ax.scatter(
                    group["Cost (₹)"],
                    group["Efficiency (%)"],
                    color=colors[panel_type],
                    label=panel_type,
                    s=50
                )
            
            ax.set_xlabel("Cost (₹)")
            ax.set_ylabel("Efficiency (%)")
            ax.legend()
            st.pyplot(fig)

if __name__ == "__main__":
    show_recommendation()
