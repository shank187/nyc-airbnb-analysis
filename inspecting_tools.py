import pandas as pd

def quick_inspect(df: pd.DataFrame):
    print(df.shape)
    print(df.info())

def check_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    nans_count = df.isnull().sum()
    nans_percent = df.isnull().mean()
    result_df = pd.concat(
        [nans_count, nans_percent],
        axis=1
    )
    result_df = result_df.rename(columns={0:'Null_Count', 1: "Percentage"})
    result_df = result_df[result_df["Null_Count"] > 0]
    return result_df

def check_unique_values(df: pd.DataFrame, min_nunique : int = 16):
    s = (df.dtypes == 'object')
    object_cols = list(s[s].index)
    print("Categorical Variables:")
    print(object_cols)
    print("\n\n")
    print(f"============== nunique <= {min_nunique} ==============")
    for col in object_cols:
        if(df[col].nunique() <= min_nunique):
            print(f"\nunique values in {col}")
            print(df[col].value_counts())
    print(f"============== nunique > {min_nunique} ==============")
    for col in object_cols:
        if(df[col].nunique() > min_nunique):
            print(f"Column {col}  contains {df[col].nunique()} uniqe value")