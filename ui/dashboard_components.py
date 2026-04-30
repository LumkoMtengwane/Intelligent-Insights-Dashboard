import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_metric_row(summary):
    cols = st.columns(4)
    cols[0].metric("Total Rows", f"{summary['rows']:,}")
    cols[1].metric("Total Columns", summary["columns"])
    cols[2].metric("Duplicate Rows", f"{summary['duplicates']:,}")
    missing_total = sum(summary["missing_values"].values())
    cols[3].metric("Missing Values", f"{missing_total:,}")


def render_data_types_table(summary):
    dt = summary["data_types"]
    df_types = pd.DataFrame(
        {
            "Column": list(dt.keys()),
            "Type": [str(v) for v in dt.values()],
            "Unique": [summary["unique_values"].get(k, "\u2014") for k in dt.keys()],
            "Missing": [summary["missing_values"].get(k, 0) for k in dt.keys()],
        }
    )
    st.dataframe(df_types, use_container_width=True, hide_index=True)


def render_quality_gauge(score):
    """Render a Plotly gauge chart for the data quality score."""
    if score >= 80:
        bar_color = "#2ecc71"
    elif score >= 50:
        bar_color = "#f39c12"
    else:
        bar_color = "#e74c3c"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " / 100", "font": {"size": 28, "color": "#191970"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#191970"},
                "bar": {"color": bar_color, "thickness": 0.7},
                "bgcolor": "#f0f2f8",
                "borderwidth": 2,
                "bordercolor": "#191970",
                "steps": [
                    {"range": [0, 50], "color": "#fce4e4"},
                    {"range": [50, 80], "color": "#fef9e7"},
                    {"range": [80, 100], "color": "#e8f8f5"},
                ],
            },
            title={"text": "Data Quality Score", "font": {"size": 16, "color": "#191970"}},
        )
    )
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=10),
        paper_bgcolor="white",
        font=dict(family="Segoe UI, Arial, sans-serif"),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_quality_breakdown(quality):
    """Render quality metrics row and detail tables."""
    c1, c2, c3 = st.columns(3)
    c1.metric("Missing", f"{quality['missing_pct']}%")
    c2.metric("Duplicates", f"{quality['duplicate_pct']}%", delta=f"{quality['duplicate_count']} rows")
    c3.metric("Outliers", f"{quality['total_outliers']:,}", delta=f"{quality['outlier_pct']}% of numeric cells")

    outliers = quality.get("outlier_counts", {})
    flagged = {k: v for k, v in outliers.items() if v > 0}
    if flagged:
        st.markdown("**Outliers by column:**")
        df_outliers = pd.DataFrame(
            {"Column": list(flagged.keys()), "Outlier Count": list(flagged.values())}
        )
        st.dataframe(df_outliers, use_container_width=True, hide_index=True)

    per_col = quality.get("per_column_missing", {})
    if per_col:
        st.markdown("**Missing values by column:**")
        df_missing = pd.DataFrame(
            {
                "Column": list(per_col.keys()),
                "Missing Count": [v["count"] for v in per_col.values()],
                "Missing %": [f"{v['pct']}%" for v in per_col.values()],
            }
        )
        st.dataframe(df_missing, use_container_width=True, hide_index=True)
