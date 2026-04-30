def format_number(number):
    if isinstance(number, (int, float)):
        if number >= 1_000_000:
            return f"{number / 1_000_000:.2f}M"
        elif number >= 1_000:
            return f"{number / 1_000:.1f}K"
    return str(number)


def get_column_types(df):
    return {
        "numeric": df.select_dtypes(include=["number"]).columns.tolist(),
        "categorical": df.select_dtypes(include=["object", "category"]).columns.tolist(),
        "datetime": df.select_dtypes(include=["datetime64"]).columns.tolist(),
    }
