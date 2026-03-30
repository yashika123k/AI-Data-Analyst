import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from data_cleaning import clean_data
from anomaly_detector import detect_anomalies
from Dashboard_engine import generate_dashboard
from smart_insights import generate_insights
from report_engine import generate_report


# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)


# ------------------------------------------------
# UI STYLE
# ------------------------------------------------

st.markdown("""
<style>

.main-title{
font-size:48px;
font-weight:700;
text-align:center;
background: linear-gradient(90deg,#4facfe,#00f2fe);
-webkit-background-clip: text;
color: transparent;
margin-bottom:30px;
}

.kpi-card{
background:white;
padding:15px;
border-radius:12px;
box-shadow:0px 3px 8px rgba(0,0,0,0.08);
text-align:center;
}

.insight-box{
background:white;
color:black;
padding:14px;
border-radius:10px;
margin-bottom:10px;
box-shadow:0px 2px 6px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown('<p class="main-title">AI Data Analyst</p>', unsafe_allow_html=True)

st.write(
"Upload a dataset and automatically generate dashboards, insights, KPIs and reports."
)


# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("Upload Dataset")

file = st.sidebar.file_uploader(
    "Upload CSV or Excel",
    type=["csv","xlsx"]
)


# ------------------------------------------------
# MAIN
# ------------------------------------------------

if file:

    # Load dataset
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df = clean_data(df)


    # ------------------------------------------------
    # KPI CARDS
    # ------------------------------------------------

    st.subheader("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Duplicates", int(df.duplicated().sum()))


    # ------------------------------------------------
    # DATA PREVIEW
    # ------------------------------------------------

    st.subheader("Dataset Preview")

    st.dataframe(df.head(), use_container_width=True)


    # ------------------------------------------------
    # COLUMN TYPE ANALYSIS
    # ------------------------------------------------

    st.subheader("Column Analysis")

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns

    c1, c2 = st.columns(2)

    with c1:
        st.write("Numeric Columns")
        st.write(list(numeric_cols))

    with c2:
        st.write("Categorical Columns")
        st.write(list(categorical_cols))


    # ------------------------------------------------
    # OUTLIER DETECTION
    # ------------------------------------------------

    st.subheader("Outlier Detection")

    anomalies = detect_anomalies(df)

    if anomalies is not None and len(anomalies) > 0:

        st.warning(f"{len(anomalies)} anomalies detected")

        st.dataframe(anomalies.head(), use_container_width=True)

    else:

        st.success("No major anomalies detected")


    # ------------------------------------------------
    # INTERACTIVE CHART BUILDER
    # ------------------------------------------------

    st.subheader("Interactive Chart Builder")

    c1, c2, c3 = st.columns(3)

    x_axis = c1.selectbox("X Axis", df.columns)

    y_axis = c2.selectbox(
        "Y Axis",
        numeric_cols if len(numeric_cols)>0 else df.columns
    )

    chart_type = c3.selectbox(
        "Chart Type",
        ["Bar","Line","Scatter"]
    )


    if chart_type == "Bar":
        fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis)

    elif chart_type == "Line":
        fig = px.line(df, x=x_axis, y=y_axis)

    else:
        fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis)

    st.plotly_chart(fig, use_container_width=True)


    # ------------------------------------------------
    # CORRELATION HEATMAP
    # ------------------------------------------------

    st.subheader("Correlation Heatmap")

    numeric_df = df.select_dtypes(include="number")

    if len(numeric_df.columns) > 1:

        corr = numeric_df.corr()

        fig = ff.create_annotated_heatmap(
            z=corr.values,
            x=list(corr.columns),
            y=list(corr.columns)
        )

        st.plotly_chart(fig, use_container_width=True)


    # ------------------------------------------------
    # AUTO DASHBOARD
    # ------------------------------------------------

    st.subheader("PowerBI Style Auto Dashboard")

    if st.button("Generate Dashboard"):

        charts = generate_dashboard(df)

        for chart in charts:

            st.plotly_chart(chart, use_container_width=True)


    # ------------------------------------------------
    # BUSINESS INSIGHTS
    # ------------------------------------------------

    st.subheader("AI Business Insights")

    insights = generate_insights(df)

    if insights:

        for i in insights[:5]:

            st.markdown(
                f'<div class="insight-box">{i}</div>',
                unsafe_allow_html=True
            )

    else:

        st.info("Not enough information for insights.")


    # ------------------------------------------------
    # NARRATIVE REPORT
    # ------------------------------------------------

    st.subheader("Narrative Business Report")

    if st.button("Generate Report"):

        report = generate_report(df)

        st.write(report)


        st.download_button(
            "Download Report",
            report,
            "report.txt"
        )


else:

    st.info("Upload a dataset to begin analysis.")