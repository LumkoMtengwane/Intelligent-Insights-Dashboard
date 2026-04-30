def generate_summary(df):
    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "unique_values": df.nunique().to_dict(),
        "summary_stats": df.describe(include="all").to_dict(),
    }
    return summary
