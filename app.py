
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tech Workflow Summary", layout="wide")

st.title("📊 Tech Daily and Overall Summary by Work Type")

uploaded_file = st.file_uploader("Upload Technician Workflow CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["Date When"] = pd.to_datetime(df["Date When"], errors="coerce")
    df = df.dropna(subset=["Date When"])
    df["Day"] = df["Date When"].dt.date

    df_daily = df.groupby(["Techinician", "Day", "Work Type"]).agg(
        Jobs_Completed=("WO#", "nunique"),
        Total_Entries=("WO#", "count"),
        Unique_Statuses=("Tech Status", pd.Series.nunique),
        Average_Duration=("Duration", lambda x: pd.to_numeric(x.str.extract(r"(\d+\.?\d*)")[0], errors="coerce").mean())
    ).reset_index()

    df_overall = df.groupby(["Techinician", "Work Type"]).agg(
        Total_Jobs=("WO#", "nunique"),
        Total_Entries=("WO#", "count"),
        Unique_Statuses=("Tech Status", pd.Series.nunique),
        Average_Duration=("Duration", lambda x: pd.to_numeric(x.str.extract(r"(\d+\.?\d*)")[0], errors="coerce").mean())
    ).reset_index()

    st.subheader("📅 Daily Summary by Work Type")
    work_types = df_daily["Work Type"].unique()
    selected_types = st.multiselect("Filter by Work Type", work_types, default=list(work_types))

    filtered_daily = df_daily[df_daily["Work Type"].isin(selected_types)]
    st.dataframe(filtered_daily, use_container_width=True)

    st.subheader("📈 Overall Average Summary by Work Type")
    st.dataframe(df_overall, use_container_width=True)
