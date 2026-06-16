import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

st.set_page_config(
    page_title="Engagement Analysis",
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

df = pd.read_csv('European_Bank.csv')

st.title("Engagement Analystics")

with st.expander("ℹ️ How is the Engagement Score Calculated?"):
    st.markdown("""
    **💳 Credit Card Engagement (Highest Impact)**  
    - Customers with a credit card receive a base engagement score of **0.5**.
    - If the customer is an active member, credit card engagement is doubled (**1.0**) because active card usage can generate frequent transactions and recurring revenue.

    **🏦 Financial Product Relationship**
    - 1 product → 0.1 points
    - 2 products → 0.2 points
    - 3 products → 0.4 points
    - 4 products → 0.7 points

    - Active members receive an additional **0.25 points** because they are more likely to actively use their financial products.

    **⏳ Customer Loyalty (Tenure)**
    - Each year with the bank contributes **0.1 points**.
    - Long-term customers are assumed to have stronger trust and a deeper relationship with the bank.

    **⚠️ Business Assumptions**
    - The dataset does not specify the exact type of financial products (loans, investments, deposits, etc.).
    - Product count is therefore used as a proxy for relationship depth.
    - Weightages are based on banking business assumptions and can be adjusted according to domain knowledge.

    **📈 Final Engagement Score**
    - The score combines card activity, product relationship, customer activity, and tenure to estimate overall customer engagement with the bank.
    """)

    
df["cc_score"] = df["HasCrCard"].apply(
    lambda x: 0.5 if x == 1 else 0
)

# Product engagement
product_map = {
    1: 0.1,
    2: 0.2,
    3: 0.4,
    4: 0.7
}

df["product_score"] = df["NumOfProducts"].map(product_map)

# Active member adjustment
df.loc[df["IsActiveMember"] == 1, "cc_score"] *= 2

df.loc[df["IsActiveMember"] == 1, "product_score"] += 0.25

# Final engagement score
df["engagement_score"] = (
    df["cc_score"] +
    df["product_score"]
)

# remove intermediate columns
df.drop(
    columns=["cc_score", "product_score"],
    inplace=True
)

df["engagement_group"] = pd.cut(
    df["engagement_score"],
    bins=[0, 0.5, 1, 1.5, 2],
    labels=["Low", "Medium", "High", "Very High"]
)

from matplotlib.ticker import FuncFormatter


# ---------------- Dark Theme Function ----------------

def dark_theme(fig, ax):
    fig.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    # Axis labels and tick colors
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.tick_params(colors="white")

    # Axis borders
    for spine in ax.spines.values():
        spine.set_color("white")

    # Title
    ax.title.set_color("white")

    # Legend styling
    if ax.get_legend():
        legend = ax.get_legend()
        legend.get_frame().set_facecolor("#111827")
        legend.get_frame().set_edgecolor("white")

        for text in legend.get_texts():
            text.set_color("white")

        legend.get_title().set_color("white")


# ---------------- Color Palette ----------------

palette = {
    0: "#2563EB",  # Stayed Customers
    1: "#6B7280"   # Exited Customers
}


# ---------------- Graph 1 ----------------

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()

    sns.countplot(
        x="engagement_group",
        hue="Exited",
        data=df,
        palette=palette,
        ax=ax
    )

    ax.set_title(
        "Customer Count by Engagement Group",
        fontsize=12,
        fontweight="bold"
    )

    ax.set_xlabel("Engagement Group")
    ax.set_ylabel("Number of Customers")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    dark_theme(fig, ax)

    st.pyplot(fig)


# ---------------- Graph 2 ----------------

with col2:
    fig, ax = plt.subplots()

    sns.barplot(
        x="engagement_group",
        y="Balance",
        hue="Exited",
        data=df,
        estimator=sum,
        palette=palette,
        ax=ax
    )

    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x/1e6:.1f}M")
    )

    ax.set_title(
        "Total Balance by Engagement Group",
        fontsize=12,
        fontweight="bold"
    )

    ax.set_xlabel("Engagement Group")
    ax.set_ylabel("Total Balance (Millions)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    dark_theme(fig, ax)

    st.pyplot(fig)


# ---------------- Graph 3 ----------------

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()

    sns.barplot(
        x="engagement_group",
        y="Balance",
        hue="Exited",
        data=df,
        palette=palette,
        ax=ax
    )

    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f"{x/1e6:.1f}M")
    )

    ax.set_title(
        "Average Balance by Engagement Group",
        fontsize=12,
        fontweight="bold"
    )

    ax.set_xlabel("Engagement Group")
    ax.set_ylabel("Average Balance (Millions)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    dark_theme(fig, ax)

    st.pyplot(fig)


# ---------------- Graph 4 ----------------

with col2:
    fig, ax = plt.subplots()

    sns.barplot(
        x="engagement_group",
        y="Age",
        hue="Exited",
        data=df,
        palette=palette,
        ax=ax
    )

    ax.set_title(
        "Average Age by Engagement Group",
        fontsize=12,
        fontweight="bold"
    )

    ax.set_xlabel("Engagement Group")
    ax.set_ylabel("Average Age")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    dark_theme(fig, ax)

    st.pyplot(fig)


