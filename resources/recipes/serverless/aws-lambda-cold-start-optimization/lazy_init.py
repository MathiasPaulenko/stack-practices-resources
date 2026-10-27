import json

# BAD: Module-level initialization — runs on every cold start
# import pandas as pd
# df = pd.read_csv('data.csv')  # 2-3 seconds

# GOOD: Lazy initialization — only runs when needed
_pd = None
_df = None

def get_pandas():
    global _pd
    if _pd is None:
        import pandas as pd
        _pd = pd
    return _pd

def get_data():
    global _df
    if _df is None:
        pd = get_pandas()
        _df = pd.read_csv('data.csv')
    return _df

def lambda_handler(event, context):
    df = get_data()
    result = df.head(10).to_dict(orient="records")
    return {
        "statusCode": 200,
        "body": json.dumps(result),
    }
