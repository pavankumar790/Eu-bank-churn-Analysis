import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

st.set_page_config(
    page_title="Age Analysis",
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


df = pd.read_csv('European_Bank.csv')

st.title("Age Analystics")

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

df_country['age_grp'] = pd.cut(df_country['Age'], [0,20,30,40,60,80,100], labels=['0-20', '20-30', '30-40', '40-50', '50-60', '60+'])
agedf=df_country.groupby('age_grp').count()['Exited'].reset_index()
agedf.rename(columns={'Exited': 'total_cust'}, inplace=True)
agedf['exited_cnt'] = df_country[df_country['Exited']==1].groupby('age_grp').count()['Exited'].reset_index()['Exited']
agedf['churnrate'] = (agedf['exited_cnt']/agedf['total_cust'].replace(0, np.nan))*100
agedf['amt_lst'] = df_country[df_country['Exited']==1].groupby('age_grp').sum()['Balance'].reset_index()['Balance']
agedf['val_per_cust_in_agegrp'] = agedf['amt_lst']/agedf['exited_cnt'].replace(0, np.nan)


col1, col2 = st.columns(2)
with col1:
    st.metric("Age group having most number of Exited people", agedf[agedf['exited_cnt'] == agedf['exited_cnt'].max()]['age_grp'].values[0], agedf['exited_cnt'].max())
    
    st.metric("Standard diveation of total customers of age grp is ", round(agedf['total_cust'].std(),2), round(agedf['total_cust'].mean(),2))

with col2:
    st.metric("Age group where avg value lost is maximum", agedf[agedf['val_per_cust_in_agegrp'] == agedf['val_per_cust_in_agegrp'].max()]['age_grp'].values[0], round(agedf['val_per_cust_in_agegrp'].max(),2))

    st.metric("Age group where maximum amount is lost", agedf[agedf['amt_lst'] == agedf['amt_lst'].max()]['age_grp'].values[0], agedf['amt_lst'].max())

from matplotlib.ticker import FuncFormatter


def dark_theme(fig, ax):
    fig.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    # Axis labels and ticks
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.tick_params(colors="white")

    # Spines
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


# --------- Graph 1 ---------

fig, ax = plt.subplots(1, 2, figsize=(10, 4))

sns.barplot(
    data=agedf,
    x="age_grp",
    y="val_per_cust_in_agegrp",
    color="#2563EB",
    ax=ax[0]
)

ax[0].set_title(
    "Average Balance per Customer by Age Group",
    color="white",
    fontsize=12,
    fontweight="bold"
)
ax[0].set_xlabel("Age Group")
ax[0].set_ylabel("Average Balance")
ax[0].spines["top"].set_visible(False)
ax[0].spines["right"].set_visible(False)


plot_df = agedf.melt(
    id_vars="age_grp",
    value_vars=["total_cust", "exited_cnt"],
    var_name="Metric",
    value_name="Count"
)

sns.barplot(
    data=plot_df,
    x="age_grp",
    y="Count",
    hue="Metric",
    palette={
        "total_cust": "#2563EB",
        "exited_cnt": "#6B7280"
    },
    ax=ax[1]
)

ax[1].set_title(
    "Total vs Exited Customers by Age Group",
    color="white",
    fontsize=12,
    fontweight="bold"
)
ax[1].set_xlabel("Age Group")
ax[1].set_ylabel("Number of Customers")
ax[1].spines["top"].set_visible(False)
ax[1].spines["right"].set_visible(False)


for a in ax:
    dark_theme(fig, a)

st.pyplot(fig)


# --------- Graph 2 ---------

fig, ax = plt.subplots(1, 2, figsize=(10, 4))

sns.barplot(
    data=agedf,
    x="age_grp",
    y="churnrate",
    color="#2563EB",
    ax=ax[0]
)

ax[0].set_title(
    "Churn Rate by Age Group",
    color="white",
    fontsize=12,
    fontweight="bold"
)
ax[0].set_xlabel("Age Group")
ax[0].set_ylabel("Churn Rate (%)")
ax[0].spines["top"].set_visible(False)
ax[0].spines["right"].set_visible(False)


sns.barplot(
    data=agedf,
    x="age_grp",
    y="amt_lst",
    color="#2563EB",
    ax=ax[1]
    
)

ax[1].yaxis.set_major_formatter(
    FuncFormatter(lambda x, pos: f"{x/1e6:.1f}M")
)

ax[1].set_title(
    "Total Balance Lost by Age Group",
    color="white",
    fontsize=12,
    fontweight="bold"
)
ax[1].set_xlabel("Age Group")
ax[1].set_ylabel("Balance Lost (Millions)")
ax[1].spines["top"].set_visible(False)
ax[1].spines["right"].set_visible(False)


for a in ax:
    dark_theme(fig, a)

st.pyplot(fig)


