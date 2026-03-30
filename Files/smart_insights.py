import pandas as pd

def generate_insights(df):

    insights = []

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns

    # ------------------------------------------------
    # DATASET SIZE INSIGHT
    # ------------------------------------------------

    insights.append(
        f"The dataset contains {df.shape[0]} records across {df.shape[1]} variables."
    )

    # ------------------------------------------------
    # NUMERIC KPI ANALYSIS
    # ------------------------------------------------

    for col in numeric_cols[:2]:

        total = df[col].sum()
        avg = df[col].mean()
        max_val = df[col].max()
        min_val = df[col].min()

        insights.append(
            f"The total {col} is {round(total,2)}, with an average value of {round(avg,2)}."
        )

        insights.append(
            f"The highest {col} observed is {round(max_val,2)} while the lowest is {round(min_val,2)}."
        )

    # ------------------------------------------------
    # CATEGORY DOMINANCE
    # ------------------------------------------------

    for col in categorical_cols[:1]:

        top = df[col].value_counts().idxmax()

        insights.append(
            f"The category '{top}' appears most frequently in {col}, indicating a dominant segment."
        )

    # ------------------------------------------------
    # TREND DETECTIONsa
    # ------------------------------------------------

    if len(numeric_cols) >= 2:

        corr = df[numeric_cols].corr()

        strong_corr = corr.unstack().sort_values(ascending=False)

        strong_corr = strong_corr[strong_corr < 0.99]

        if len(strong_corr) > 0:

            pair = strong_corr.index[0]

            insights.append(
                f"There is a strong relationship between {pair[0]} and {pair[1]}, suggesting potential predictive influence."
            )

    return insights