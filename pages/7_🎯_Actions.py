import streamlit as st

st.subheader("🎯 Actions to be Taken")

with st.expander("View Recommended Actions", expanded=True):
    st.markdown("""
- Prioritize customer retention initiatives in Germany.
- Investigate the reasons behind high churn among customers aged 40–50.
- Develop targeted retention programs for high-value customers in France and Spain.
- Analyze customers holding four products to identify potential product-related issues.
- Improve engagement strategies for high-value inactive customers.
- Re-evaluate the effectiveness of credit card ownership and tenure-based retention mechanisms.
- Introduce personalized offers and loyalty programs for high-risk customer segments.
- Monitor churn trends regularly to assess the effectiveness of retention initiatives.
""")