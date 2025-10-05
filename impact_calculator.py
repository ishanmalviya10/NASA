import streamlit as st

# Page config
st.set_page_config(page_title="AQI Impact Calculator", layout="wide")

st.title("🌍 AQI Impact Calculator")
st.write("Quantify the economic & health value of air quality interventions")

# Sidebar Input Parameters
st.sidebar.header("⚙️ Input Parameters")
population = st.sidebar.number_input("Population", value=5000000, step=100000)
baselineAQI = st.sidebar.number_input("Baseline AQI", value=180)
targetAQI = st.sidebar.number_input("Target AQI (Post-Intervention)", value=120)
avgDailyWage = st.sidebar.number_input("Avg Daily Wage ($)", value=150)
hospitalAdmissionCost = st.sidebar.number_input("Hospital Admission Cost ($)", value=2500)
baselineAdmissions = st.sidebar.number_input("Baseline Admissions (Annual)", value=1000)
systemCost = st.sidebar.number_input("System Implementation Cost ($)", value=1000000)

# --- Calculations ---
pm25Reduction = (baselineAQI - targetAQI) * 0.6  # Rough conversion AQI to PM2.5
populationExposed = population * 0.75  # 75% urban exposure

# Health Impact
admissionsAvoided = round(baselineAdmissions * (pm25Reduction / baselineAQI) * 0.15)
healthcareSavings = admissionsAvoided * hospitalAdmissionCost

# Productivity Impact
sickDaysReduction = 2  # days per person annually
productivityGain = round(populationExposed * 0.6 * sickDaysReduction)  # 60% workforce
productivityValue = productivityGain * avgDailyWage

# Social Cost (WHO methodology)
socialCostPerPerson = (pm25Reduction / 10) * 50
totalSocialValue = populationExposed * socialCostPerPerson

# Compliance & Economic
complianceDaysGained = round((pm25Reduction / baselineAQI) * 365 * 0.2)
finesAvoided = complianceDaysGained * 50000

# Total Benefits & ROI
totalBenefits = healthcareSavings + productivityValue + totalSocialValue + finesAvoided
roi = round((totalBenefits - systemCost) / systemCost, 2)
paybackMonths = round((systemCost / totalBenefits) * 12)

# --- Layout ---
st.markdown("## 📊 Investment Return Analysis")
col1, col2, col3 = st.columns(3)
col1.metric("ROI", f"{roi}:1")
col2.metric("Payback Period", f"{paybackMonths} months")
col3.metric("Net Benefit", f"${(totalBenefits - systemCost)/1e6:.1f}M")

# Health Impact
st.markdown("## ❤️ Health Impact")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Admissions Avoided", f"{admissionsAvoided}")
col2.metric("Healthcare Savings", f"${healthcareSavings/1e6:.2f}M")
col3.metric("PM2.5 Reduction", f"{pm25Reduction:.1f} μg/m³")
col4.metric("Population Protected", f"{populationExposed/1e6:.2f}M")

# Economic Impact
st.markdown("## 💵 Economic Impact")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Productivity Days Saved", f"{productivityGain:,}")
col2.metric("Productivity Value", f"${productivityValue/1e6:.2f}M")
col3.metric("Compliance Days Gained", f"{complianceDaysGained}")
col4.metric("Fines Avoided", f"${finesAvoided/1e6:.2f}M")

# Benefits Breakdown
st.markdown("## 📈 Total Annual Benefits Breakdown")
st.write(f"- Healthcare Savings: **${healthcareSavings/1e6:.2f}M**")
st.write(f"- Productivity Value: **${productivityValue/1e6:.2f}M**")
st.write(f"- Social Cost Savings: **${totalSocialValue/1e6:.2f}M**")
st.write(f"- Compliance Benefits: **${finesAvoided/1e6:.2f}M**")
st.success(f"**TOTAL BENEFITS: ${(totalBenefits/1e6):.2f}M**")

# Stakeholder Value Proposition
st.markdown("## 👥 Stakeholder Value Proposition")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Healthcare Systems", f"{admissionsAvoided} Admissions Avoided")
col2.metric("Businesses & Industry", f"${productivityValue/1e6:.1f}M Productivity")
col3.metric("Regulatory Agencies", f"{complianceDaysGained} Compliance Days")
col4.metric("Citizens & Communities", f"{populationExposed/1e6:.1f}M People Protected")

# Key Insights
st.markdown("## 💡 Key Insights")
st.info(f"**Economic Efficiency**: Every $1 invested returns ${roi} in benefits, with payback in {paybackMonths} months.")
st.info(f"**Health Protection**: Prevents {admissionsAvoided} hospital admissions annually, reducing system burden.")
st.info("**Multi-Stakeholder Value**: Benefits span healthcare, industry, government, and citizens.")

# Notes
st.markdown("---")
st.markdown("📌 *Data sources: WHO, OECD, World Bank, peer-reviewed health economics literature*")
