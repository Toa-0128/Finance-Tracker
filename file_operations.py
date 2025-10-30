def save_to_csv(df, filename):
    """
    df: pandas DataFrame
    filename: name of the CSV file to save
    """
    try:
        df.to_csv(filename, index=False)
        print(f"Transactions saved to {filename} successfully!")
    except Exception as e:
        print(f"Error saving file: {e}")
