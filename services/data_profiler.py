import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.chart_theme import apply_midnight_theme


def profile_dataset(df):
    """Return correlation matrix, skewness dict, and distribution figures for numeric columns."""
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    corr_matrix = df[numeric_cols].corr() if len(numeric_cols) >= 2 else pd.DataFrame()
    skewness = df[numeric_cols].skew().round(3).to_dict() if numeric_cols else {}

    distributions = []
    for col in numeric_cols[:8]:
        fig = px.histogram(
            df,
            x=col,
            marginal="box",
            title=f"Distribution of {col}",
            histnorm="probability density",
        )
        apply_midnight_theme(fig)
        fig.update_layout(height=350)
        distributions.append(fig)

    return {
        "correlation_matrix": corr_matrix,
        "skewness": skewness,
        "distributions": distributions,
    }


def build_correlation_heatmap(corr_matrix):
    """Build a Plotly heatmap from a correlation matrix."""
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.columns.tolist(),
            colorscale=[
                [0, "#4a90d9"],
                [0.5, "white"],
                [1, "#191970"],
            ],
            zmin=-1,
            zmax=1,
            text=corr_matrix.values.round(2),
            texttemplate="%{text}",
            textfont=dict(size=11),
        )
    )
    apply_midnight_theme(fig)
    fig.update_layout(title="Correlation Heatmap", height=500)
    return fig
