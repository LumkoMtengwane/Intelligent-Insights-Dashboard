def validate_csv(df):
    warnings = []

    if df.shape[0] == 0:
        warnings.append("Dataset has no rows.")
    if df.shape[1] == 0:
        warnings.append("Dataset has no columns.")
    if 0 < df.shape[0] < 2:
        warnings.append("Dataset has very few rows \u2014 insights may be limited.")

    total_cells = df.shape[0] * df.shape[1]
    if total_cells > 0:
        missing_pct = (df.isnull().sum().sum() / total_cells) * 100
        if missing_pct > 30:
            warnings.append(f"High percentage of missing values: {missing_pct:.1f}%")

    dup_count = df.duplicated().sum()
    if dup_count > 0:
        warnings.append(f"Found {dup_count} duplicate rows.")

    return warnings
