import streamlit as st

def show_subsidy_page():
# Title
    st.markdown("<h2 style='text-align: center;'>💰 State-wise Solar Subsidy Information</h2>", unsafe_allow_html=True)
    st.markdown("### 📍 Select your state or union territory to view available subsidies and application methods")

# Subsidy data
    subsidy_info = {
    "Andhra Pradesh": [
        "🏠 Central Subsidy: 40% up to 3kW, 20% beyond",
        "⚡ Net metering policy active",
        "🔗 DISCOM: APSPDCL, APEPDCL – Online portal available"
    ],
    "Arunachal Pradesh": [
        "🏠 Central Subsidy: 40%",
        "⚡ Limited DISCOM reach; solar adoption encouraged",
        "🔗 Apply via Department of Power"
    ],
    "Assam": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering through Assam Power Distribution Company",
        "🔗 Apply via APDCL portal"
    ],
    "Bihar": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering available via NBPDCL & SBPDCL",
        "🔗 BREDA manages rooftop solar projects"
    ],
    "Chhattisgarh": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via CSPDCL",
        "🔗 Online applications accepted"
    ],
    "Delhi": [
        "🏠 Central Subsidy: 40% up to 3kW, 20% beyond",
        "⚡ Net metering available",
        "🏢 State DISCOM: BSES, TPDDL provide online application portals"
    ],
    "Goa": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering under Goa Electricity Dept.",
        "🔗 Apply via Goa Energy Development Agency (GEDA)"
    ],
    "Gujarat": [
        "🏠 Central Subsidy + State Subsidy: ₹10,000/kW (up to 2kW)",
        "⚡ Net metering policy highly active",
        "🔗 Apply via GEDA Portal"
    ],
    "Haryana": [
        "🏠 Central Subsidy: 40% + State Incentives",
        "⚡ Net metering supported by UHBVN & DHBVN",
        "🔗 Apply via Haryana Solar Portal"
    ],
    "Himachal Pradesh": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via HPSEB",
        "🔗 Apply through HIMURJA"
    ],
    "Jharkhand": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering supported by JBVNL",
        "🔗 Apply via JREDA Portal"
    ],
    "Karnataka": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering available through BESCOM & others",
        "🔗 Apply via KREDL or DISCOM websites"
    ],
    "Kerala": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering managed by KSEB",
        "🔗 Apply via KSEB Solar Portal"
    ],
    "Madhya Pradesh": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via MP DISCOMs",
        "🔗 Apply via MP Urja Vikas Nigam"
    ],
    "Maharashtra": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering through MSEDCL",
        "🔗 Online application portal available"
    ],
    "Manipur": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering implementation underway",
        "🔗 Contact MANIREDA"
    ],
    "Meghalaya": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering through MePDCL",
        "🔗 Apply via MePDCL site"
    ],
    "Mizoram": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering slowly rolling out",
        "🔗 Contact Power & Electricity Dept., Mizoram"
    ],
    "Nagaland": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering limited",
        "🔗 Contact Department of New & Renewable Energy"
    ],
    "Odisha": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via TPCODL, NESCO, etc.",
        "🔗 Apply via OREDA"
    ],
    "Punjab": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via PSPCL",
        "🔗 Apply via PEDA Portal"
    ],
    "Rajasthan": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via JVVNL, AVVNL, JDVVNL",
        "🔗 Apply via RRECL"
    ],
    "Sikkim": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering available",
        "🔗 Apply via Sikkim Renewable Energy Development Agency"
    ],
    "Tamil Nadu": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via TANGEDCO",
        "🔗 Apply via TEDA website"
    ],
    "Telangana": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering available via TSNPDCL & TSSPDCL",
        "🔗 Apply via TSREDCO"
    ],
    "Tripura": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering available",
        "🔗 Apply via TREDA"
    ],
    "Uttar Pradesh": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via UPPCL",
        "🔗 Apply via UP NEDA portal"
    ],
    "Uttarakhand": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering supported",
        "🔗 Apply via UREDA portal"
    ],
    "West Bengal": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via WBSEDCL",
        "🔗 Apply via WBREDA"
    ],
    "Andaman and Nicobar Islands": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via local dept.",
        "🔗 Contact Electricity Dept., Andaman"
    ],
    "Chandigarh": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering available",
        "🔗 Apply via CREST: https://crestchandigarh.org.in/"
    ],
    "Dadra and Nagar Haveli and Daman and Diu": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering as per local rules",
        "🔗 Apply via DISCOM"
    ],
    "Ladakh": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering for Leh & Kargil",
        "🔗 Contact LREDA"
    ],
    "Jammu and Kashmir": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering available",
        "🔗 Apply via JAKEDA"
    ],
    "Lakshadweep": [
        "🏠 Central Subsidy: 40%",
        "⚡ Limited metering options",
        "🔗 Contact UT Energy Department"
    ],
    "Puducherry": [
        "🏠 Central Subsidy: 40%",
        "⚡ Net metering via PED",
        "🔗 Apply via Electricity Department"
    ]
}

# Dropdown
    state = st.selectbox("🔎 Select your State/UT", sorted(subsidy_info.keys()))

# Display info
    if state:
        st.markdown(f"### ☀️ Subsidy Details for **{state}**")
        for item in subsidy_info[state]:
            st.markdown(f"- {item}")
    
        st.markdown("#### Eligibility Checklist:")
        c1 = st.checkbox("You are an Indian resident")
        c2 = st.checkbox("You have ownership of the property")
        c3 = st.checkbox("You have not already claimed solar subsidy")
        c4 = st.checkbox("You are applying through the official portal")

        if c1 and c2 and c3 and c4:
            st.success("✅ You are eligible for subsidy!")
            st.markdown("[👉 Apply Here](https://solarrooftop.gov.in)", unsafe_allow_html=True)
            st.markdown("#### 📄 Required Documents:")
            st.markdown("- Aadhar Card")
            st.markdown("- Electricity Bill")
            st.markdown("- Property Ownership Proof")
            st.markdown("- Bank Account Details")
        else:
            st.warning("Please complete all eligibility requirements.")
    # Back to Home button
    st.markdown("---")
    if st.button("🔙 Back to Home"):
        st.session_state["nav"] = "home"
        st.rerun()


show_subsidy_page()
