import plotly.express as px


def generate_dashboard(df):

    charts = []

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns

    # Chart 1: Histogram
    if len(numeric_cols) > 0:

        fig = px.histogram(
            df,
            x=numeric_cols[0],
            title=f"Distribution of {numeric_cols[0]}"
        )

        charts.append(fig)

    # Chart 2: Bar chart
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:

        fig = px.bar(
            df,
            x=categorical_cols[0],
            y=numeric_cols[0],
            color=categorical_cols[0],
            title=f"{numeric_cols[0]} by {categorical_cols[0]}"
        )

        charts.append(fig)

    # Chart 3: Scatter
    if len(numeric_cols) >= 2:

        fig = px.scatter(
            df,
            x=numeric_cols[0],
            y=numeric_cols[1],
            title=f"{numeric_cols[0]} vs {numeric_cols[1]}"
        )

        charts.append(fig)

    return charts
