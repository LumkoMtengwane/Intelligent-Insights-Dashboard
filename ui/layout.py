import streamlit as st

MIDNIGHT = "#191970"
SECONDARY = "#1e3a5f"
ACCENT = "#4a90d9"
SURFACE = "#f0f2f8"


def apply_page_config():
    st.set_page_config(
        layout="wide",
        page_title="Insights Dashboard",
        page_icon="\U0001F4CA",
        initial_sidebar_state="expanded",
    )


def inject_custom_css():
    st.markdown(
        f"""
    <style>
    /* ── Global ─────────────────────────────────────────── */
    .main .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 1rem;
    }}
    h1, h2, h3 {{
        color: {MIDNIGHT} !important;
    }}

    /* ── Metric cards ───────────────────────────────────── */
    div[data-testid="stMetric"] {{
        background: linear-gradient(135deg, {MIDNIGHT} 0%, {SECONDARY} 100%);
        padding: 16px 20px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 16px rgba(25, 25, 112, 0.25);
    }}
    div[data-testid="stMetric"] label {{
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.85rem !important;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        color: white !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {{
        color: rgba(255,255,255,0.7) !important;
    }}

    /* ── Tabs ───────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        background-color: {SURFACE};
        border-radius: 10px;
        padding: 5px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        color: {SECONDARY};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {MIDNIGHT} !important;
        color: white !important;
        box-shadow: 0 2px 10px rgba(25,25,112,0.3);
    }}

    /* ── Sidebar ────────────────────────────────────────── */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {MIDNIGHT} 0%, {SECONDARY} 60%, #0d2137 100%);
    }}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown li {{
        color: white !important;
    }}
    section[data-testid="stSidebar"] label {{
        color: rgba(255,255,255,0.9) !important;
    }}
    section[data-testid="stSidebar"] .stMetric label,
    section[data-testid="stSidebar"] div[data-testid="stMetricValue"] {{
        color: white !important;
    }}

    /* ── Expanders ──────────────────────────────────────── */
    .streamlit-expanderHeader {{
        font-weight: 600;
        font-size: 1rem;
        color: {MIDNIGHT};
    }}

    /* ── Plotly containers ──────────────────────────────── */
    .stPlotlyChart {{
        border: 1px solid #e0e4ec;
        border-radius: 12px;
        overflow: hidden;
    }}

    /* ── Buttons ────────────────────────────────────────── */
    .stButton > button {{
        background: linear-gradient(135deg, {MIDNIGHT} 0%, {SECONDARY} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: opacity 0.2s;
    }}
    .stButton > button:hover {{
        opacity: 0.9;
    }}

    /* ── Download buttons ───────────────────────────────── */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {ACCENT} 0%, {MIDNIGHT} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }}

    /* ── Dataframes ─────────────────────────────────────── */
    .stDataFrame {{
        border-radius: 10px;
        overflow: hidden;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )
