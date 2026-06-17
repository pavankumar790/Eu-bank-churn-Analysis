import streamlit as st

st.markdown("""
<style>

/* Entire sidebar background */
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

/* Sidebar navigation area */
div[data-testid="stSidebarNav"] {
    background-color: #111827 !important;
    padding-top: 20px;
}

/* Each page button */
a[data-testid="stSidebarNavLink"] {
    background-color: #1F2937 !important;
    color: white !important;
    border-radius: 12px !important;
    margin: 8px 10px !important;
    padding: 12px 15px !important;
    transition: 0.3s;
}

/* Page text */
a[data-testid="stSidebarNavLink"] p {
    color: white !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}

/* Emoji */
a[data-testid="stSidebarNavLink"] span[data-testid="stIconEmoji"] {
    font-size: 18px !important;
}

/* Hover effect */
a[data-testid="stSidebarNavLink"]:hover {
    background-color: #2563EB !important;
}

/* Selected/current page */
a[data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: #2563EB !important;
    box-shadow: 0 0 10px rgba(37, 99, 235, 0.5);
}

/* Selected page text */
a[data-testid="stSidebarNavLink"][aria-current="page"] p {
    color: white !important;
    font-weight: 700 !important;
}

/* Collapse arrow */
button[data-testid="stBaseButton-headerNoPadding"] {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

st.subheader("📌 Summary")

with st.expander("View Summary", expanded=True):
    st.markdown("""
- Germany has the highest churn rate (~32%) and the highest average balance lost per churned customer (~120K).    - France and Spain have lower churn rates (~16%) and lower average balance loss per churned customer (~70K).
- Overall churn rate is approximately 20%.
- Total balance lost due to customer churn is approximately €185.59M.
- Customers aged 40–50 exhibit the highest churn rates across all countries.
- Customers aged 30–40 form the largest customer segment and demonstrate the strongest retention.
- High-value customers contribute a disproportionate share of total balance lost when they churn.
- Despite Germany having the highest overall churn rate, high-value customers exhibit a lower churn rate (29.4%) compared to non-high-value customers (34.4%), indicating relatively stronger retention among valuable customers.
- High-value customers contribute a smaller share of balance loss in Germany compared to France and Spain, suggesting that the financial impact of high-value customer churn is less concentrated in Germany.             
- Customer engagement metrics show weaker-than-expected relationships with customer retention.
- All customers holding four products were observed to have churned, representing a significant anomaly.
""")
    
