import streamlit as st
import pandas as pd
from utils.validators import validate_csv
from services.query_engine import run_nl_query


def render_sidebar():
    """Render sidebar: branding, upload, dataset info, filters, and chat panel."""
    with st.sidebar:
        # ── Branding ────────────────────────────────────────────────────
        st.markdown("## \U0001F4CA Insights Dashboard")
        st.markdown("---")
        st.markdown("Upload a CSV to get automated analysis, charts, and AI insights.")

        uploaded_file = st.file_uploader(
            "Upload CSV File",
            type=["csv"],
            accept_multiple_files=False,
            help="Upload a .csv file to analyze",
        )

        # ── Dataset info + filters ──────────────────────────────────────
        if uploaded_file and "data" in st.session_state:
            df = st.session_state["data"]
            st.markdown("---")
            st.markdown("### Dataset Info")
            col1, col2 = st.columns(2)
            col1.metric("Rows", f"{df.shape[0]:,}")
            col2.metric("Columns", df.shape[1])

            warnings = validate_csv(df)
            if warnings:
                for w in warnings:
                    st.warning(w, icon="\u26A0\uFE0F")

            st.markdown("---")
            st.markdown("### Filters")

            all_cols = df.columns.tolist()
            selected_cols = st.multiselect(
                "Columns to include",
                all_cols,
                default=all_cols,
                help="Select columns for analysis",
            )

            row_limit = st.slider(
                "Row limit",
                min_value=10,
                max_value=df.shape[0],
                value=min(df.shape[0], 5000),
                step=10,
                help="Limit rows for faster analysis on large datasets",
            )

            filtered = df[selected_cols].head(row_limit) if selected_cols else df.head(row_limit)
            st.session_state["data_filtered"] = filtered

            # ── Chat panel ──────────────────────────────────────────────
            st.markdown("---")
            st.markdown("### Chat With Your Data")

            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []

            chat_container = st.container(height=300)
            with chat_container:
                for msg in st.session_state["chat_history"]:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
                        if msg.get("code"):
                            with st.expander("Code", expanded=False):
                                st.code(msg["code"], language="python")

            question = st.chat_input("Ask your data a question...")
            if question:
                st.session_state["chat_history"].append(
                    {"role": "user", "content": question}
                )
                result = run_nl_query(filtered, question)
                if result["error"]:
                    answer_text = f"Error: {result['error']}"
                    code = result.get("code", "")
                else:
                    answer = result["answer"]
                    if isinstance(answer, (pd.DataFrame, pd.Series)):
                        answer_text = answer.to_string()
                    else:
                        answer_text = str(answer)
                    code = result.get("code", "")

                st.session_state["chat_history"].append(
                    {"role": "assistant", "content": answer_text, "code": code}
                )

                if "query_log" not in st.session_state:
                    st.session_state["query_log"] = []
                st.session_state["query_log"].append(
                    {"question": question, "answer": answer_text, "code": code}
                )
                st.rerun()

        # ── Footer ──────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown(
            "<div style='text-align:center; opacity:0.5; font-size:0.75rem;'>"
            "Built with Streamlit + Azure OpenAI"
            "</div>",
            unsafe_allow_html=True,
        )

    return uploaded_file
