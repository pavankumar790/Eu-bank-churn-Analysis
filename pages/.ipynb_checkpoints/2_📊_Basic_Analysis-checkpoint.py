import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(
    page_title="Basic Analysis",
    #page_icon="assets/icon.png", 
    layout="wide",
    initial_sidebar_state="collapsed")

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

st.set_page_config(layout="wide")

st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #374151;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Increase height of segmented control buttons */
button[data-testid="stBaseButton-segmented_control"],
button[data-testid="stBaseButton-segmented_controlActive"] {
    height: 70px !important;
    font-size: 20px !important;
    border-radius: 12px !important;
}

/* Make the text larger */
button[data-testid="stBaseButton-segmented_control"] p,
button[data-testid="stBaseButton-segmented_controlActive"] p {
    font-size: 18px !important;
    font-weight: 600;
}
            
/* Selected button */
button[data-testid="stBaseButton-segmented_controlActive"] {
    color: black !important;
    font-weight: 700 !important;
    background-color: #2563EB !important;
    border-color: #2563EB !important;
}

/* Increase space around the whole control */
div[data-testid="stButtonGroup"] {
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)



st.title("Eu Bank Analysis")

df = pd.read_csv('European_Bank.csv')

country_name = st.segmented_control(
    "",
    list(df["Geography"].unique()) + ["all"],width="stretch",default="all"
)

def country(x):
    if x == 'all':
        return(df)
    else:
        dfx=df[df['Geography']==x]
        return(dfx)
def tot_pop(x):
    n = x['Exited'].count()
    return(n)
def tot_pop_exit(x):
    n = x[x['Exited']==1]['Exited'].count()
    return(n)
def bal_lost(x):
    n = x[x['Exited']==1]['Balance'].sum()
    return(n)
def avg_bal_lost(x):
    n = x[x['Exited']==1]['Balance'].mean()
    return(n)

df_country = country(country_name)

col5, col6 = st.columns([1,3])

with col5:
    overall_churn = (tot_pop_exit(df) / tot_pop(df)) * 100
    country_churn = (tot_pop_exit(df_country) / tot_pop(df_country)) * 100

    st.metric("Overall Churn", round(((tot_pop_exit(df) / tot_pop(df)) * 100),2))
    st.metric("Country Churn", round(((tot_pop_exit(df_country) / tot_pop(df_country)) * 100),2))
    st.metric("Country Churn", round(((tot_pop_exit(df_country) / tot_pop(df)) * 100),2))

with col6:
    overall_churn = (tot_pop_exit(df) / tot_pop(df)) * 100
    country_churn = (tot_pop_exit(df_country) / tot_pop(df_country)) * 100

    fig2 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=overall_churn,
    title={'text': "Overall vs Country Churn"},
    gauge={
        'axis': {'range': [0, 100]},
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'value': country_churn
            }
        }
    )   )
    st.plotly_chart(fig2)


col1, col2 = st.columns(2)
with col1:
    st.metric("Total Customers", tot_pop(df_country))
    st.metric("Exited Customers", tot_pop_exit(df_country))
    st.metric("Balance Lost", round(bal_lost(df_country), 2))
    st.metric("Avg Balance Lost", round(avg_bal_lost(df_country), 2))

with col2:
    fig, ax = plt.subplots()
    sns.countplot(data=df_country, x='Exited', ax=ax, color="#2563EB")

    for container in ax.containers:
        ax.bar_label(container)
    
    # Background colors
    fig.set_facecolor("#0E1117")   # Outer figure background
    ax.set_facecolor("#0E1117")    # Plot area background

    # Make labels and ticks white
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.tick_params(colors="white")
    ax.set_xticklabels(["Stayed", "Exited"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_title(
    "Customer Churn Distribution",
    color="white",
    fontsize=14,
    fontweight="bold"
    )

    # Make borders white
    for spine in ax.spines.values():
        spine.set_color("white")

    # Make bar labels white
    for container in ax.containers:
        ax.bar_label(container, color="white")

    st.pyplot(fig)
    
