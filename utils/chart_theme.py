MIDNIGHT_COLORS = [
    "#191970", "#4a90d9", "#1e3a5f", "#6baed6",
    "#2c5282", "#90cdf4", "#1a365d", "#bee3f8",
]


def apply_midnight_theme(fig):
    """Apply a consistent Midnight Blue theme to any Plotly figure."""
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Segoe UI, Arial, sans-serif", color="#1e3a5f"),
        title_font=dict(size=18, color="#191970", family="Segoe UI, Arial, sans-serif"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        colorway=MIDNIGHT_COLORS,
        margin=dict(l=40, r=30, t=60, b=40),
        xaxis=dict(
            gridcolor="#e0e4ec",
            linecolor="#c0c8d8",
            title_font=dict(color="#1e3a5f"),
            tickfont=dict(color="#1e3a5f"),
        ),
        yaxis=dict(
            gridcolor="#e0e4ec",
            linecolor="#c0c8d8",
            title_font=dict(color="#1e3a5f"),
            tickfont=dict(color="#1e3a5f"),
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#e0e4ec",
            borderwidth=1,
        ),
    )
    return fig
