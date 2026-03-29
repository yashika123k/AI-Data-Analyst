# AI Data Analyst 📊

**AI Data Analyst** is an interactive Streamlit application that allows users to upload datasets and automatically generate dashboards, KPIs, business insights, anomaly detection, and narrative reports. This tool is designed to accelerate data exploration and empower decision-makers with actionable intelligence.

---

## Features

- **Dataset Overview** – Get rows, columns, missing values, and duplicates metrics.
- **Data Cleaning** – Automatic duplicate removal and column standardization.
- **Outlier Detection** – Identify anomalies using z-score based method.
- **Interactive Charts** – Build bar, line, and scatter charts dynamically.
- **Correlation Heatmap** – Visualize relationships between numeric variables.
- **Auto Dashboard** – Generate multiple Plotly charts like a PowerBI-style dashboard.
- **AI Business Insights** – Summarizes key numeric and categorical insights.
- **Narrative Report** – Generate a textual report summarizing the dataset.

---

## Installation

```bash
git clone https://github.com/yourusername/ai-data-analyst.git
cd ai-data-analyst
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
