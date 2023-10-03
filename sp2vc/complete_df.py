import pandas as pd

def complete_df(df):
    """
    Generates a DataFrame with all possible combinations of unique values for each column.

    Given a DataFrame, this function produces a new DataFrame where each column contains
    all the possible combinations of its unique values with the unique values of other columns.
    Essentially, it computes the Cartesian product of unique values across all columns.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: A new DataFrame containing all possible combinations of unique values
                    from the input DataFrame's columns.

    Example:
    from sp2vc import *
    import pandas as pd
    df = pd.DataFrame({
        'x': [2020, 2020, 2021],
        'y': [1, 3, 1],
        'z': [10, 20, 30]
    })
    completed_df = complete_df(df)
    print(completed_df)

    Notes:
    - The order of rows in the resulting DataFrame is determined by the order of unique values 
      in the input columns.
    """
    # Get column names
    cols_to_complete = df.columns
    # Generate all possible combinations
    unique_values = [df[col].unique() for col in cols_to_complete]
    completed = pd.MultiIndex.from_product(unique_values, names = cols_to_complete)
    completed_df = completed.to_frame(index = False)
    return completed_df
