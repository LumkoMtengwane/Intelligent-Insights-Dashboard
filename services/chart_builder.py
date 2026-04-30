import plotly.express as px
from utils.chart_theme import apply_midnight_theme

CHART_TYPES = ["bar", "line", "scatter", "pie", "box", "histogram"]


def build_chart(df, chart_type, x_col=None, y_col=None):
    chart_type = chart_type.lower()

    if chart_type == "bar":
        fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Chart: {x_col} vs {y_col}")
    elif chart_type == "line":
        fig = px.line(df, x=x_col, y=y_col, title=f"Line Chart: {x_col} vs {y_col}")
    elif chart_type == "scatter":
        fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
    elif chart_type == "pie":
        fig = px.pie(df, values=y_col, names=x_col, title=f"Pie Chart: {x_col}")
    elif chart_type == "box":
        fig = px.box(df, x=x_col, y=y_col, title=f"Box Plot: {x_col} vs {y_col}")
    elif chart_type == "histogram":
        fig = px.histogram(df, x=x_col, title=f"Histogram: {x_col}")
    else:
        raise ValueError(f"Unsupported chart type: '{chart_type}'. Choose from: {CHART_TYPES}")

    apply_midnight_theme(fig)
    return fig
