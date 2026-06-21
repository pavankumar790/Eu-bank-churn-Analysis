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

df = pd.read_csv('European_Bank.csv')

st.title("Engagement Analystics")

page = st.segmented_control(
    "",
    [
        "📊 Customer Attribute Analysis",
        "📈 Engagement Analysis"
    ],
    default="📊 Customer Attribute Analysis",
    width="stretch"
)

if page == "📊 Customer Attribute Analysis":

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Churn rate of customers having credit card ", round(100*(df[df['HasCrCard']==1]['Exited'].mean()),2))
    
        st.metric("Churn rate of customers not having credit card ", round(100*(df[df['HasCrCard']==0]['Exited'].mean()),2))

    with col2:
        st.metric("Churn rate of active members", round(100*(df[df['IsActiveMember']==1]['Exited'].mean()),2))

        st.metric("Churn rate of in-active members", round(100*(df[df['IsActiveMember']==0]['Exited'].mean()),2))
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()

        sns.countplot(
            x="HasCrCard",
            hue="Exited",
            data=df,
            palette=palette,
            ax=ax
        )

        ax.set_title(
            "Customers exited credit Card",
            fontsize=12,
            fontweight="bold"
        )

        ax.set_xlabel("Credit card")
        ax.set_ylabel("No of customers")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%d",
                padding=3,
                color="white",
                fontsize=10
            )

        dark_theme(fig, ax)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()

        sns.countplot(
            x="IsActiveMember",
            hue="Exited",
            data=df,
            palette=palette,
            ax=ax
        )

        ax.set_title(
            "Customers exited Active members",
            fontsize=12,
            fontweight="bold"
        )

        ax.set_xlabel("Active Member")
        ax.set_ylabel("No of customers")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%d",
                padding=3,
                color="white",
                fontsize=10
            )

        dark_theme(fig, ax)
        st.pyplot(fig)

    col1, col2, col3 = st.columns(3)

    with col1:
        fig, ax = plt.subplots()

        bins = [300, 400, 500, 600, 700, 800, 900]

        sns.histplot(
            x="CreditScore",
            hue="Exited",
            data=df,
            multiple="dodge",
            palette=palette,
            bins=bins,
            ax=ax
        )

        centers = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins)-1)]
        labels = ["300-399", "400-499", "500-599",
                  "600-699", "700-799", "800-899"]

        ax.set_xticks(centers)
        ax.set_xticklabels(labels)

        ax.set_title(
            "Credit score effect on exited",
            fontsize=12,
            fontweight="bold"
        )

        ax.set_xlabel("Credit Score")
        ax.set_ylabel("No of customers")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%d",
                padding=3,
                color="white",
                fontsize=10
            )

        dark_theme(fig, ax)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()

        sns.histplot(
            x="Tenure",
            hue="Exited",
            data=df,
            multiple="dodge",
            discrete=True,
            palette=palette,
            ax=ax,
            bins=10
        )

        ax.set_xticks(sorted(df["Tenure"].unique()))

        ax.set_title(
            "Tenure effect on exited",
            fontsize=12,
            fontweight="bold"
        )

        ax.set_xlabel("Tenure")
        ax.set_ylabel("No of customers")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%d",
                padding=3,
                color="white",
                fontsize=10
            )

        dark_theme(fig, ax)
        st.pyplot(fig)

    with col3:
        fig, ax = plt.subplots()

        sns.histplot(
            x="NumOfProducts",
            hue="Exited",
            data=df,
            multiple="dodge",
            discrete=True,
            palette=palette,
            ax=ax,
            bins=4
        )

        ax.set_xticks(sorted(df["NumOfProducts"].unique()))

        ax.set_title(
            "Products effect on exited",
            fontsize=12,
            fontweight="bold"
        )

        ax.set_xlabel("Number of Products")
        ax.set_ylabel("No of customers")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%d",
                padding=3,
                color="white",
                fontsize=10
            )

        dark_theme(fig, ax)
        st.pyplot(fig)


elif page == "📈 Engagement Analysis":
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

        **⚠️ Business Assumptions**
        - The dataset does not specify the exact type of financial products.
        - Product count is used as a proxy for relationship depth.
        - Weightages are based on banking business assumptions.

        **📈 Final Engagement Score**
        - The score combines card activity and product relationship to estimate overall customer engagement.
        """)

    df["cc_score"] = df["HasCrCard"].apply(
        lambda x: 0.5 if x == 1 else 0
    )

    product_map = {
        1: 0.1,
        2: 0.2,
        3: 0.4,
        4: 0.7
    }

    df["product_score"] = df["NumOfProducts"].map(product_map)

    df.loc[df["IsActiveMember"] == 1, "cc_score"] *= 2
    df.loc[df["IsActiveMember"] == 1, "product_score"] += 0.25

    df["engagement_score"] = (
        df["cc_score"] +
        df["product_score"]
    )

    df.drop(
        columns=["cc_score", "product_score"],
        inplace=True,
        errors="ignore"
    )

    df["engagement_group"] = pd.cut(
        df["engagement_score"],
        bins=[0, 0.5, 1, 1.5, 2],
        labels=["Low", "Medium", "High", "Very High"]
    )

    from matplotlib.ticker import FuncFormatter

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
        ax.set_ylabel("Average Balance")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        dark_theme(fig, ax)
        st.pyplot(fig)

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