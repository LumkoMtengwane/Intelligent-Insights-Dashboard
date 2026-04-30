import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from ui.layout import apply_page_config, inject_custom_css
from ui.sidebar import render_sidebar
from ui.dashboard_components import (
    render_metric_row,
    render_data_types_table,
    render_quality_gauge,
    render_quality_breakdown,
)
from services.data_loader import load_csv
from services.data_summary import generate_summary
from services.data_quality import run_quality_check
from services.data_profiler import profile_dataset, build_correlation_heatmap
from services.chart_generator import generate_basic_charts
from services.chart_builder import build_chart, CHART_TYPES
from services.insights_engine import generate_insights
from services.report_generator import generate_report_pdf
from services.blob_storage import upload_chart
from services.ml_recommender import detect_task_type, suggest_models
from utils.helpers import get_column_types

load_dotenv()
apply_page_config()
inject_custom_css()

# ── Sidebar: upload, filters, chat ──
uploaded_file = render_sidebar()

if uploaded_file:
    df = load_csv(uploaded_file)
    st.session_state["data"] = df

    if "query_log" not in st.session_state:
        st.session_state["query_log"] = []
    if "insights_text" not in st.session_state:
        st.session_state["insights_text"] = None
    if "charts_cache" not in st.session_state:
        st.session_state["charts_cache"] = None

    df_filtered = st.session_state.get("data_filtered", df)
    summary = generate_summary(df_filtered)
    quality = run_quality_check(df_filtered)
    col_types = get_column_types(df_filtered)

    st.title("Intelligent Insights Dashboard")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "\U0001F4CB  Overview",
            "\U0001F50D  Quality & Profiling",
            "\U0001F4CA  Charts",
            "\U0001F9E0  AI Insights & ML",
            "\U0001F4C4  Reports",
        ]
    )

    # ═══════════════════════════════════════════════════════════════════
    # TAB 1 — Overview
    # ═══════════════════════════════════════════════════════════════════
    with tab1:
        st.subheader("Key Metrics")
        render_metric_row(summary)

        st.markdown("")
        gauge_col, preview_col = st.columns([1, 3])

        with gauge_col:
            render_quality_gauge(quality["quality_score"])

        with preview_col:
            with st.expander("Preview Data (first 20 rows)", expanded=True):
                st.dataframe(df_filtered.head(20), use_container_width=True, hide_index=True)

        with st.expander("Column Details"):
            render_data_types_table(summary)

        with st.expander("Statistical Summary"):
            st.dataframe(df_filtered.describe(include="all").T, use_container_width=True)

    # ═══════════════════════════════════════════════════════════════════
    # TAB 2 — Quality & Profiling
    # ═══════════════════════════════════════════════════════════════════
    with tab2:
        st.subheader("Data Quality")
        render_quality_breakdown(quality)

        st.markdown("---")
        st.subheader("Dataset Profiling")

        profile = profile_dataset(df_filtered)

        if not profile["correlation_matrix"].empty:
            heatmap_fig = build_correlation_heatmap(profile["correlation_matrix"])
            st.plotly_chart(heatmap_fig, use_container_width=True)

        if profile["skewness"]:
            with st.expander("Skewness of Numeric Columns", expanded=True):
                skew_df = pd.DataFrame(
                    {"Column": list(profile["skewness"].keys()),
                     "Skewness": list(profile["skewness"].values())}
                )
                st.dataframe(skew_df, use_container_width=True, hide_index=True)

        if profile["distributions"]:
            st.subheader("Feature Distributions")
            dist_cols = st.columns(2)
            for i, fig in enumerate(profile["distributions"]):
                with dist_cols[i % 2]:
                    st.plotly_chart(fig, use_container_width=True)

    # ═══════════════════════════════════════════════════════════════════
    # TAB 3 — Charts
    # ═══════════════════════════════════════════════════════════════════
    with tab3:
        quick_section, custom_section = st.tabs(
            ["Quick Auto-Charts", "Custom Chart Builder"]
        )

        with quick_section:
            st.subheader("Auto-Generated Charts")
            if st.session_state["charts_cache"] is None:
                st.session_state["charts_cache"] = generate_basic_charts(df_filtered)

            charts = st.session_state["charts_cache"]
            if charts:
                chart_cols = st.columns(2)
                for i, chart in enumerate(charts):
                    with chart_cols[i % 2]:
                        st.plotly_chart(chart, use_container_width=True)
            else:
                st.info("No auto-charts could be generated for this dataset.")

        with custom_section:
            st.subheader("Build Your Own Chart")

            b1, b2, b3 = st.columns(3)
            with b1:
                chart_type = st.selectbox("Chart Type", CHART_TYPES)
            with b2:
                x_col = st.selectbox("X-axis Column", df_filtered.columns.tolist())
            with b3:
                y_options = ["(none)"] + col_types["numeric"]
                y_selection = st.selectbox("Y-axis Column", y_options)
                y_col = None if y_selection == "(none)" else y_selection

            btn1, btn2 = st.columns(2)
            with btn1:
                generate_btn = st.button("Generate Chart", use_container_width=True)
            with btn2:
                save_btn = st.button("Save to Cloud", use_container_width=True)

            if generate_btn:
                try:
                    fig = build_chart(df_filtered, chart_type, x_col, y_col)
                    st.plotly_chart(fig, use_container_width=True)
                    st.session_state["last_custom_chart"] = fig
                    st.session_state["last_chart_params"] = {
                        "chart_type": chart_type, "x_col": x_col, "y_col": y_col
                    }
                except Exception as e:
                    st.error(f"Could not generate chart: {e}")

            if save_btn:
                if "last_chart_params" not in st.session_state:
                    st.warning("Generate a chart first before saving.")
                else:
                    with st.spinner("Uploading to Azure Blob Storage..."):
                        try:
                            p = st.session_state["last_chart_params"]
                            fig = build_chart(df_filtered, p["chart_type"], p["x_col"], p["y_col"])
                            result = upload_chart(fig)
                        except Exception as e:
                            result = {"success": False, "error": str(e)}
                    if result.get("success"):
                        st.success(f"Saved! URL: {result['url']}")
                    else:
                        st.error(f"Upload failed: {result.get('error', 'Unknown error')}")

    # ═════════════════════════
    # TAB 4 — AI Insights & ML
    # ═════════════════════════
    with tab4:
        insights_sec, ml_sec = st.tabs(["AI Insights", "ML Model Suggestions"])

        with insights_sec:
            st.subheader("AI-Powered Insights")
            st.markdown("Generate intelligent insights about your dataset using Azure OpenAI.")

            c1, c2 = st.columns(2)
            with c1:
                gen_btn = st.button("Generate Insights", use_container_width=True)
            with c2:
                regen_btn = st.button("Regenerate", use_container_width=True)

            if gen_btn or regen_btn:
                with st.spinner("Analyzing your data with AI..."):
                    try:
                        text = generate_insights(df_filtered)
                        st.session_state["insights_text"] = text
                    except Exception as e:
                        st.error(f"Failed to generate insights: {e}")

            if st.session_state["insights_text"]:
                st.markdown("---")
                st.markdown(st.session_state["insights_text"])

        with ml_sec:
            st.subheader("ML Model Recommendations")
            st.markdown("Select a target column (or leave blank for unsupervised) and get top 3 model suggestions.")

            target_options = ["(none -- unsupervised)"] + df_filtered.columns.tolist()
            target_selection = st.selectbox("Target Column", target_options)
            target_col = None if target_selection.startswith("(none") else target_selection

            if st.button("Suggest Models", use_container_width=True):
                task_info = detect_task_type(df_filtered, target_col)

                st.info(f"**Detected task:** {task_info['task_type']}  \n{task_info['reason']}")

                with st.spinner("Consulting AI for model recommendations..."):
                    try:
                        models = suggest_models(df_filtered, task_info)
                    except Exception as e:
                        st.error(f"Failed: {e}")
                        models = []

                if models:
                    m_cols = st.columns(3)
                    for i, m in enumerate(models[:3]):
                        with m_cols[i]:
                            st.markdown(f"### {i + 1}. {m.get('name', 'Model')}")
                            st.markdown(f"**Why:** {m.get('why', '')}")
                            st.markdown(f"**Tune:** `{m.get('hyperparameters', '')}`")
                            st.markdown(f"**Note:** {m.get('considerations', '')}")

    # ═══════════════════════════════════════════════════════════════════
    # TAB 5 — Reports
    # ═══════════════════════════════════════════════════════════════════
    with tab5:
        st.subheader("Generate PDF Report")
        st.markdown(
            "Create a comprehensive multipage PDF report with your data summary, "
            "quality analysis, charts, AI insights, and query history."
        )

        if st.button("Generate Report", use_container_width=True, key="gen_report"):
            with st.spinner("Building PDF report..."):
                all_charts = st.session_state.get("charts_cache") or []
                pdf_bytes = generate_report_pdf(
                    summary=summary,
                    quality=quality,
                    chart_figures=all_charts,
                    insights=st.session_state.get("insights_text"),
                    query_log=st.session_state.get("query_log"),
                )
                st.session_state["report_pdf"] = pdf_bytes

        if "report_pdf" in st.session_state:
            st.markdown("---")

            st.markdown("### Report Contents")
            st.markdown(f"- **Cover page** with quality score ({quality['quality_score']}/100)")
            st.markdown(f"- **Data Summary** ({summary['rows']:,} rows, {summary['columns']} columns)")
            st.markdown(f"- **Data Quality** (missing {quality['missing_pct']}%, {quality['total_outliers']} outliers)")
            n_charts = len(st.session_state.get("charts_cache") or [])
            st.markdown(f"- **{n_charts} Charts**")
            has_insights = "Yes" if st.session_state.get("insights_text") else "No"
            st.markdown(f"- **AI Insights:** {has_insights}")
            n_queries = len(st.session_state.get("query_log") or [])
            st.markdown(f"- **{n_queries} Queries** in history")

            st.download_button(
                label="Download Report as PDF",
                data=st.session_state["report_pdf"],
                file_name="insights_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

else:
    # ── Landing page ────────────────────────────────────────────────────
    st.title("Intelligent Insights Dashboard")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### \U0001F4C1 Upload")
        st.markdown("Upload a CSV file using the sidebar to get started.")
    with c2:
        st.markdown("### \U0001F4CA Analyze")
        st.markdown("Get summaries, quality scores, charts, and AI insights.")
    with c3:
        st.markdown("### \U0001F4C4 Report")
        st.markdown("Generate multipage PDF reports with all your findings.")

    st.markdown("---")
    st.info("Use the sidebar on the left to upload a CSV file and begin your analysis.")
