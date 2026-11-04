import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv("data/orders.csv")
ProfileReport(df, title="Orders Dataset Profile", minimal=True).to_file("reports/orders_profile.html")

def profile_dataframe(df):
    p = {"row_count": len(df), "column_count": len(df.columns), "null_counts": df.isnull().sum().to_dict(), "duplicate_rows": int(df.duplicated().sum()), "dtypes": df.dtypes.astype(str).to_dict()}
    for c in df.select_dtypes(include="number").columns:
        p[c] = {"min": float(df[c].min()), "max": float(df[c].max()), "mean": float(df[c].mean()), "std": float(df[c].std())}
    return p

if __name__ == "__main__":
    print(profile_dataframe(df)["row_count"])
