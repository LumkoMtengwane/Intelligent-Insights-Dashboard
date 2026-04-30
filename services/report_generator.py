import tempfile
import os
from datetime import datetime
from fpdf import FPDF


class _ReportPDF(FPDF):
    """Custom FPDF subclass with consistent header/footer styling."""

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(25, 25, 112)
        self.cell(0, 8, "Intelligent Insights Dashboard  |  Data Report", align="R")
        self.ln(10)
        self.set_draw_color(25, 25, 112)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, text):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(25, 25, 112)
        self.ln(6)
        self.cell(0, 10, text)
        self.ln(12)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def key_value(self, key, value):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 58, 95)
        self.cell(60, 7, f"{key}:")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(0, 7, str(value))
        self.ln(7)


def generate_report_pdf(summary, quality=None, chart_figures=None, insights=None, query_log=None):
    """Build a multipage PDF report and return it as bytes."""
    pdf = _ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── Page 1: Cover ───────────────────────────────────────────────────
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(25, 25, 112)
    pdf.cell(0, 15, "Data Insights Report", align="C")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}", align="C")
    pdf.ln(10)
    if quality:
        pdf.set_font("Helvetica", "B", 20)
        score = quality.get("quality_score", "N/A")
        pdf.set_text_color(25, 25, 112)
        pdf.cell(0, 12, f"Data Quality Score: {score} / 100", align="C")
    pdf.ln(15)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"{summary.get('rows', 0):,} rows  x  {summary.get('columns', 0)} columns", align="C")

    # ── Page 2: Data Summary ────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title("Data Summary")
    pdf.key_value("Total Rows", f"{summary.get('rows', 0):,}")
    pdf.key_value("Total Columns", summary.get("columns", 0))
    pdf.key_value("Duplicate Rows", f"{summary.get('duplicates', 0):,}")

    missing = summary.get("missing_values", {})
    total_missing = sum(missing.values())
    pdf.key_value("Total Missing Values", f"{total_missing:,}")

    if summary.get("data_types"):
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(25, 25, 112)
        pdf.cell(0, 8, "Column Types")
        pdf.ln(8)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(30, 30, 30)
        for col_name, dtype in summary["data_types"].items():
            m = missing.get(col_name, 0)
            line = f"{col_name}  ({dtype})"
            if m > 0:
                line += f"  -- {m} missing"
            pdf.cell(0, 5, line)
            pdf.ln(5)

    # ── Page 3: Data Quality ────────────────────────────────────────────
    if quality:
        pdf.add_page()
        pdf.section_title("Data Quality")
        pdf.key_value("Quality Score", f"{quality.get('quality_score', 'N/A')} / 100")
        pdf.key_value("Missing Values", f"{quality.get('missing_pct', 0)}%")
        pdf.key_value("Duplicate Rows", f"{quality.get('duplicate_pct', 0)}%  ({quality.get('duplicate_count', 0)} rows)")
        pdf.key_value("Total Outliers", f"{quality.get('total_outliers', 0)}")
        pdf.ln(4)

        outliers = quality.get("outlier_counts", {})
        if outliers:
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(25, 25, 112)
            pdf.cell(0, 8, "Outliers Per Column")
            pdf.ln(8)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(30, 30, 30)
            for col_name, count in outliers.items():
                if count > 0:
                    pdf.cell(0, 5, f"{col_name}: {count} outliers")
                    pdf.ln(5)

    # ── Pages 4+: Charts ────────────────────────────────────────────────
    if chart_figures:
        for i, fig in enumerate(chart_figures):
            try:
                img_bytes = fig.to_image(format="png", width=1000, height=500)
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    tmp.write(img_bytes)
                    tmp_path = tmp.name
                pdf.add_page()
                pdf.section_title(f"Chart {i + 1}")
                pdf.image(tmp_path, x=15, w=pdf.w - 30)
                os.unlink(tmp_path)
            except Exception:
                continue

    # ── Page N: AI Insights ─────────────────────────────────────────────
    if insights:
        pdf.add_page()
        pdf.section_title("AI-Generated Insights")
        safe = insights.encode("latin-1", errors="replace").decode("latin-1")
        pdf.body_text(safe)

    # ── Page N+1: Query History ─────────────────────────────────────────
    if query_log:
        pdf.add_page()
        pdf.section_title("Query History")
        for idx, entry in enumerate(query_log, 1):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(25, 25, 112)
            pdf.cell(0, 7, f"Q{idx}: {entry.get('question', 'N/A')}")
            pdf.ln(7)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 6, f"A: {entry.get('answer', 'N/A')}")
            pdf.set_font("Courier", "", 8)
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(0, 5, f"Code: {entry.get('code', '')}")
            pdf.ln(4)

    return pdf.output()
