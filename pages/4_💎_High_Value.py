import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Value Analysis",
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

st.title("Value Analystics")

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


select_country = st.segmented_control(
    "",
    list(df["Geography"].unique()) + ["all"],width="stretch",default="all"
)

def country(x):
    if x=="all":
        return(df)
    else:
        return(df[df['Geography']==x])
    
df_country = country(select_country)

select_Val = st.segmented_control(
    "",
    ['Balance', 'EstimatedSalary'],width="stretch",default="Balance"
)

col1, col2 = st.columns([4,1])

with col1:
    with st.container(border=True):
        threshold = st.slider(
            "High-value customer cutoff",
            50, 99, 65,
            help="Customers are ranked by value. The top customers whose cumulative value reaches this percentage are marked as high-value."
        )


with col2:
    st.metric("Value", f"{threshold}%")

threshold = threshold*0.01

def high_value_sel(x, y, z):
    df2=z[['CustomerId','Surname','Balance','EstimatedSalary','Exited','Geography']]
    df2 = df2.sort_values(x, ascending=False)
    df2['cumsumbal'] = df2[x].cumsum()
    a = df2[df2['cumsumbal']<((df2[x].sum())*y)]
    val_thb = a[x].min()
    dfh=z.copy()
    dfh['High_value'] = np.where(dfh[x] > val_thb, 1, 0)
    return(dfh, val_thb)

re = high_value_sel(select_Val, threshold, df_country)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Customers", len(re[0]))
    st.metric("Total High Value Customers", re[0][(re[0]['High_value']==1)]['Exited'].count())
    st.metric("Total High Value Customers exited", re[0][(re[0]['Exited']==1) & (re[0]['High_value']==1)]['Exited'].count())
with col2:
    st.metric("Balance Lost due to High Value Customers exit", round((re[0][(re[0]['Exited']==1) & (re[0]['High_value']==1)]['Balance'].sum()), 2))
    st.metric("Balance Lost due to normal Customers exit", round((re[0][(re[0]['Exited']==1) & (re[0]['High_value']==0)]['Balance'].sum()), 2))
    st.metric("Avg Balance Lost due to High Value Customers exit", round((re[0][(re[0]['Exited']==1) & (re[0]['High_value']==1)]['Balance'].mean()), 2))

col1, col2 = st.columns(2)

def dark_theme(fig, ax):
    fig.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    # Axis labels and ticks
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.tick_params(colors="white")

    # Borders
    for spine in ax.spines.values():
        spine.set_color("white")

    # Title
    ax.title.set_color("white")

    # Legend
    if ax.get_legend():
        legend = ax.get_legend()
        legend.get_frame().set_facecolor("#111827")
        legend.get_frame().set_edgecolor("white")

        for text in legend.get_texts():
            text.set_color("white")

        legend.get_title().set_color("white")


# ----------------- Graph 1 -----------------

with col1:
    fig1, ax = plt.subplots()

    sns.countplot(
        data=re[0][re[0]["Exited"] == 1],
        x="High_value",
        color="#2563EB",
        ax=ax
    )

    # Change 0/1 to meaningful labels
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Normal Value", "High Value"])

    # Bar values
    for container in ax.containers:
        ax.bar_label(
            container,
            color="white",
            fontsize=10
        )

    ax.set_title(
        "Exited Customers by Customer Value Segment",
        fontsize=12,
        fontweight="bold"
    )

    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Number of Exited Customers")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    dark_theme(fig1, ax)

    st.pyplot(fig1)


# ----------------- Graph 2 -----------------

with col2:
    fig2, ax2 = plt.subplots()

    normal_lost = re[0][
        (re[0]["Exited"] == 1) &
        (re[0]["High_value"] == 0)
    ]["Balance"].sum()

    high_lost = re[0][
        (re[0]["Exited"] == 1) &
        (re[0]["High_value"] == 1)
    ]["Balance"].sum()

    ax2.pie(
        [normal_lost, high_lost],
        labels=[
            "Normal Customers",
            "High Value Customers"
        ],
        colors=[
            "#6B7280",  # gray
            "#2563EB"   # blue
        ],
        autopct="%1.1f%%",
        startangle=90,
        textprops={
            "color": "white",
            "fontsize": 10
        }
    )

    fig2.set_facecolor("#0E1117")
    ax2.set_facecolor("#0E1117")

    ax2.set_title(
        "Distribution of Balance Lost by Customer Segment",
        color="white",
        fontsize=12,
        fontweight="bold"
    )

    st.pyplot(fig2)


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