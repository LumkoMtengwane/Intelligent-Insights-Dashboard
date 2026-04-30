import numpy as np


def run_quality_check(df):
    """Compute data quality metrics: missing %, duplicate %, outlier counts, and a composite score."""
    total_cells = df.shape[0] * df.shape[1]
    missing_pct = (df.isnull().sum().sum() / total_cells * 100) if total_cells > 0 else 0.0
    duplicate_pct = (df.duplicated().sum() / df.shape[0] * 100) if df.shape[0] > 0 else 0.0

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    outlier_counts = {}
    total_outliers = 0

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        n_outliers = int(((df[col] < lower) | (df[col] > upper)).sum())
        outlier_counts[col] = n_outliers
        total_outliers += n_outliers

    total_numeric_cells = df.shape[0] * len(numeric_cols) if numeric_cols else 1
    outlier_pct = total_outliers / total_numeric_cells * 100

    missing_penalty = min(missing_pct, 100)
    duplicate_penalty = min(duplicate_pct, 100)
    outlier_penalty = min(outlier_pct * 2, 100)

    quality_score = 100 - (
        0.4 * missing_penalty + 0.3 * duplicate_penalty + 0.3 * outlier_penalty
    )
    quality_score = round(max(0, min(100, quality_score)), 1)

    per_column_missing = {}
    for col in df.columns:
        count = int(df[col].isnull().sum())
        if count > 0:
            per_column_missing[col] = {
                "count": count,
                "pct": round(count / df.shape[0] * 100, 1),
            }

    return {
        "missing_pct": round(missing_pct, 2),
        "duplicate_pct": round(duplicate_pct, 2),
        "duplicate_count": int(df.duplicated().sum()),
        "outlier_counts": outlier_counts,
        "total_outliers": total_outliers,
        "outlier_pct": round(outlier_pct, 2),
        "quality_score": quality_score,
        "per_column_missing": per_column_missing,
    }
