import pandas as pd


def load_csv(file):
    df = pd.read_csv(file)
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_datetime(df[col], format="mixed")
            except (ValueError, TypeError):
                pass
    return df
