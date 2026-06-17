import streamlit as st

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
    
