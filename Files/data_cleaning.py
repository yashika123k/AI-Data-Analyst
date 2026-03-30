def clean_data(df):
    df=df.drop_duplicates()

    df.columns=df.columns.str.lower()

    return df