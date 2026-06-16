import streamlit as st

st.set_page_config(
    page_title="European Bank Churn Analytics",
    #page_icon="assets/icon.png", 
    layout="wide",
    initial_sidebar_state="collapsed")


st.title("European Bank Analytics Dashboard")

st.write(
    "Use the sidebar to select an analytics page."
)


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