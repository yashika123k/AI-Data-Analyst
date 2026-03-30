import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from data_cleaning import clean_data
from anomaly_detector import detect_anomalies
from dashboard_engine import generate_dashboard
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

/* Animated Gradient Title */

.main-title{
font-size:90px !important;
font-weight:900;
text-align:center;
background: linear-gradient(270deg,#4facfe,#00f2fe,#43e97b,#38f9d7);
background-size:600% 600%;
-webkit-background-clip:text;
color:transparent;
animation: gradientMove 8s ease infinite;
margin-bottom:5px;
}

@keyframes gradientMove{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

.sub-title{
font-size:22px;
text-align:center;
color:#6c757d;
margin-bottom:20px;
}

.divider{
height:4px;
width:160px;
margin:auto;
background: linear-gradient(90deg,#4facfe,#00f2fe);
border-radius:10px;
margin-bottom:40px;
}


/* Glass KPI Cards */

.kpi-card{
background: rgba(255,255,255,0.75);
backdrop-filter: blur(10px);
border-radius:14px;
padding:20px;
text-align:center;
border:1px solid rgba(0,0,0,0.05);
box-shadow:0 8px 25px rgba(0,0,0,0.1);
}

.kpi-title{
font-size:18px;
font-weight:600;
color:#333;
margin-bottom:6px;
}

.kpi-value{
font-size:36px;
font-weight:800;
color:#111;
}


/* Insight Box */

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

st.markdown(
'<p class="sub-title">Upload your dataset and instantly generate dashboards, insights, KPIs and business reports</p>',
unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


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

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Rows</div>
            <div class="kpi-value">{df.shape[0]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Columns</div>
            <div class="kpi-value">{df.shape[1]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Missing Values</div>
            <div class="kpi-value">{int(df.isnull().sum().sum())}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Duplicates</div>
            <div class="kpi-value">{int(df.duplicated().sum())}</div>
        </div>
        """, unsafe_allow_html=True)


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
