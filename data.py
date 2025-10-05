import streamlit as st

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(page_title="Stakeholder KPI Matrix", layout="wide")

st.title("📊 Stakeholder-KPI Mapping Matrix")
st.write(
    "Connecting air quality alerts to measurable outcomes across the entire decision-making ecosystem"
)

# --------------------
# SUMMARY STATS
# --------------------
st.markdown("### 📌 Summary Stats")
cols = st.columns(4)
cols[0].metric("Key Stakeholders", "6")
cols[1].metric("Measurable KPIs", "24")
cols[2].metric("Alert Lead Time", "48-72hr")
cols[3].metric("Average ROI", "12:1")

# --------------------
# DATA
# --------------------
stakeholders = [
    {
        "name": "Air Quality Regulatory Boards",
        "role": "Ensure compliance & protect public health",
        "decisionTrigger": "AQI >100 or trending upward",
        "interventions": [
            "Issue public health advisories",
            "Enforce industrial emission restrictions",
            "Activate emergency response protocols",
            "Coordinate multi-agency response",
        ],
        "kpis": [
            {"metric": "Compliance Days", "target": "+20-30 days/year", "impact": "High"},
            {"metric": "PM2.5 Reduction", "target": "8-12% seasonal", "impact": "High"},
            {"metric": "Public Awareness Reach", "target": "70%+ population", "impact": "Medium"},
            {"metric": "Enforcement Actions", "target": "-25% violations", "impact": "High"},
        ],
    },
    {
        "name": "Healthcare Systems & Hospitals",
        "role": "Optimize resources & minimize preventable admissions",
        "decisionTrigger": "AQI >150 forecast (48-72hr)",
        "interventions": [
            "Pre-deploy respiratory specialists",
            "Stock emergency medications & oxygen",
            "Activate surge capacity protocols",
            "Coordinate ambulance services",
        ],
        "kpis": [
            {"metric": "Admissions Avoided", "target": "10-15% reduction", "impact": "High"},
            {"metric": "Healthcare Cost Savings", "target": "$1.5-3M annually", "impact": "High"},
            {"metric": "ER Wait Time", "target": "-30% during alerts", "impact": "Medium"},
            {"metric": "Staff Overtime", "target": "-20-25%", "impact": "Medium"},
        ],
    },
    {
        "name": "Traffic Management Authorities",
        "role": "Reduce vehicular emissions during pollution episodes",
        "decisionTrigger": "AQI >180 or rapid deterioration",
        "interventions": [
            "Implement odd-even vehicle schemes",
            "Restrict heavy diesel vehicles",
            "Enhance public transit capacity",
            "Optimize traffic flow with AI routing",
        ],
        "kpis": [
            {"metric": "PM2.5 Reduction", "target": "10-18% within 48hrs", "impact": "High"},
            {"metric": "Traffic Volume Decrease", "target": "30-40%", "impact": "High"},
            {"metric": "Public Compliance Rate", "target": "75%+ voluntary", "impact": "Medium"},
            {"metric": "Commute Time Savings", "target": "15-20 min avg", "impact": "Low"},
        ],
    },
    {
        "name": "Educational Institutions",
        "role": "Protect vulnerable children & maintain learning",
        "decisionTrigger": "AQI >150 during school hours",
        "interventions": [
            "Cancel/move outdoor activities indoors",
            "Distribute masks to students",
            "Activate hybrid learning options",
            "Communicate with parents via app",
        ],
        "kpis": [
            {"metric": "Student Days Preserved", "target": "25K-40K days", "impact": "High"},
            {"metric": "Attendance Rate", "target": "Maintained at 95%+", "impact": "Medium"},
            {"metric": "Health Incidents", "target": "-40-50%", "impact": "High"},
            {"metric": "Parental Satisfaction", "target": "85%+ approval", "impact": "Medium"},
        ],
    },
    {
        "name": "Industrial Operations",
        "role": "Maintain production while meeting regulations",
        "decisionTrigger": "AQI >200 or enforcement window",
        "interventions": [
            "Schedule planned maintenance shutdowns",
            "Adjust production schedules",
            "Implement temporary emission controls",
            "Coordinate across supply chain",
        ],
        "kpis": [
            {"metric": "Fines Avoided", "target": "$800K-2M annually", "impact": "High"},
            {"metric": "Compliance Rate", "target": "95%+ clean days", "impact": "High"},
            {"metric": "Operational Efficiency", "target": "+15% planned vs emergency", "impact": "Medium"},
            {"metric": "Reputation Score", "target": "Maintained/improved", "impact": "Low"},
        ],
    },
    {
        "name": "General Public & Workforce",
        "role": "Protect health & maintain productivity",
        "decisionTrigger": "Personalized alerts via app",
        "interventions": [
            "Modify outdoor activity patterns",
            "Use protective masks when needed",
            "Work from home options",
            "Adjust commute timing",
        ],
        "kpis": [
            {"metric": "Sick Days Avoided", "target": "1-2 days/person/year", "impact": "High"},
            {"metric": "Productivity Value", "target": "$200-400/person", "impact": "High"},
            {"metric": "Health Behavior Change", "target": "60%+ adoption", "impact": "Medium"},
            {"metric": "App Engagement", "target": "70%+ active users", "impact": "Low"},
        ],
    },
]

# --------------------
# HELPER: KPI COLOR
# --------------------
def impact_color(impact: str) -> str:
    if impact == "High":
        return "🔴 High"
    elif impact == "Medium":
        return "🟡 Medium"
    elif impact == "Low":
        return "🟢 Low"
    return "⚪ Neutral"

# --------------------
# STAKEHOLDER CARDS
# --------------------
for s in stakeholders:
    st.markdown(f"## {s['name']}")
    st.write(f"**Role:** {s['role']}")
    st.write(f"**Decision Trigger:** {s['decisionTrigger']}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Alert-Driven Interventions:**")
        for i in s["interventions"]:
            st.markdown(f"- {i}")

    with col2:
        st.markdown("**Key Performance Indicators:**")
        for k in s["kpis"]:
            st.markdown(f"- **{k['metric']}** → {k['target']} ({impact_color(k['impact'])})")

# =====================================
# DISPLAY STAKEHOLDERS
# =====================================
st.markdown("## 👥 Stakeholders")

for stakeholder in stakeholders:
    st.subheader(stakeholder["name"])
    st.write("**Role:**", stakeholder["role"])
    st.write("**Decision Trigger:**", stakeholder["decisionTrigger"])
    
    # Interventions
    st.markdown("**🔹 Interventions:**")
    for intervention in stakeholder["interventions"]:
        st.markdown(f"- {intervention}")
    
    # KPIs
    st.markdown("**📈 KPIs:**")
    for kpi in stakeholder["kpis"]:
        st.markdown(f"- **{kpi['metric']}**: {kpi['target']} ({kpi['impact']})")
    
    st.markdown("---")  # horizontal divider
# --------------------
# CROSS-STAKEHOLDER IMPACT
# --------------------
st.markdown("### 🌍 Cross-Stakeholder Impact Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💰 Economic Value Chain")
    st.write("- Healthcare: $1.5-3M savings annually")
    st.write("- Productivity: $4-8M preserved value")
    st.write("- Compliance: $1-3M fines avoided")
    st.write("- Education: $1-2M value protected")
    st.metric("Total Annual Benefits", "$8.5-18M")

with col2:
    st.subheader("❤️ Health Protection")
    st.write("- 350-500 admissions avoided")
    st.write("- 3-5M people protected")
    st.write("- 8-12% PM2.5 reduction")
    st.write("- 10-15% health impact decrease")
    st.success("Lives Saved = Primary Outcome")

with col3:
    st.subheader("🎯 Operational Efficiency")
    st.write("- 48-72hr advance planning")
    st.write("- Coordinated multi-agency response")
    st.write("- +20-30 compliance days")
    st.write("- 75%+ stakeholder engagement")
    st.info("Proactive vs. Reactive Response")

# --------------------
# SUCCESS FACTORS & QUICK WINS
# --------------------
st.markdown("### ✅ Critical Success Factors & ⚡ Quick Wins")
col1, col2 = st.columns(2)

with col1:
    st.write("**Critical Success Factors**")
    st.write("- Alert Accuracy: 80%+ forecast reliability")
    st.write("- Stakeholder Buy-in: Active participation")
    st.write("- Data Infrastructure: Real-time monitoring")
    st.write("- Policy Support: Regulatory backing")
    st.write("- Public Communication: Clear messaging")

with col2:
    st.write("**Quick Wins (First 3 Months)**")
    st.write("- Hospital ER preparedness → improved capacity")
    st.write("- School activity adjustments → fewer incidents")
    st.write("- Traffic restrictions → measurable PM2.5 drops")
    st.write("- Industrial compliance → fewer violations")
    st.write("- Public awareness → 70%+ engagement")

# --------------------
# FOOTER
# --------------------
st.markdown("---")
st.subheader("📌 The Bottom Line")
st.write(
    "This framework transforms environmental satellite data into **boardroom-ready business intelligence**. "
    "Every stakeholder sees measurable value. Every alert drives coordinated action. Every intervention saves lives and money."
)

c1, c2, c3 = st.columns(3)
c1.metric("Return on Investment", "12:1")
c2.metric("Payback Period", "6-12mo")
c3.metric("Lives Protected", "5M+")

st.caption("📊 Interactive dashboard for hackathon presentation — Methodology: WHO guidelines, OECD social cost framework, peer-reviewed health economics")
