import plotly.express as px
from utils.chart_theme import apply_midnight_theme


def generate_basic_charts(df):
    """Auto-generate charts for numeric and categorical columns."""
    charts = []
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    for col in numeric_cols[:4]:
        fig = px.histogram(df, x=col, title=f"Distribution of {col}")
        fig.update_layout(bargap=0.1)
        apply_midnight_theme(fig)
        charts.append(fig)

    for col in categorical_cols[:3]:
        value_counts = df[col].value_counts().head(10).reset_index()
        value_counts.columns = [col, "Count"]
        fig = px.bar(value_counts, x=col, y="Count", title=f"Top Values in {col}")
        apply_midnight_theme(fig)
        charts.append(fig)

    if len(numeric_cols) >= 2:
        fig = px.scatter(
            df, x=numeric_cols[0], y=numeric_cols[1],
            title=f"{numeric_cols[0]} vs {numeric_cols[1]}",
        )
        apply_midnight_theme(fig)
        charts.append(fig)

    return charts
