def generate_report(df):

    rows, cols = df.shape

    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns

    report = f"""
EXECUTIVE SUMMARY

This dataset contains {rows} observations and {cols} variables.
The data provides insight into key operational metrics and categorical segments.

Key Findings:

• The dataset includes numerical metrics such as {', '.join(numeric_cols[:3])} which appear to represent core performance indicators.

• Categorical attributes such as {', '.join(categorical_cols[:3])} allow segmentation of the dataset into meaningful business groups.

• Initial statistical exploration suggests variability in numerical features, indicating potential patterns worth investigating.

Business Interpretation:

The dataset appears suitable for performance analysis, trend identification, and operational decision support.

Strategic Recommendation:

Organizations should focus on the key numerical indicators identified above and investigate drivers behind the highest and lowest performing observations. Additional segmentation analysis may reveal high-performing categories or segments.

Conclusion:

Overall, the dataset provides a strong foundation for business intelligence analysis, enabling data-driven strategic insights.
"""

    return report