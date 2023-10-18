import inspect

def map_df(df, fun):
    """
    Apply a given function to a DataFrame based on column names as arguments.
    
    This function tries to map each row of the DataFrame to the given function `fun`, 
    using the columns of the DataFrame as arguments for the function. It checks if 
    the column names of the DataFrame match the argument names of the function before 
    attempting to apply the function.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - fun (function): The function to apply to the DataFrame's rows. 
                      The function's arguments should match the DataFrame's column names.

    Returns:
    - list: The result of applying `fun` to each row of the DataFrame if column names match 
            function arguments.
    - str: An error message if there's an exception during the mapping or if the column names 
           do not match the function arguments.

    Example:
    from sp2vc import *
    import pandas as pd
    def example_fun(x, y, z):
        return x + y*2 + z*3
    
    df = pd.DataFrame({
        'x': [2020, 2020, 2021],
        'y': [1, 3, 1],
        'z': [10, 20, 30]
    })
    result = map_df(df, example_fun)
    print(df)
    print(result)

    Notes:
    - The order of the columns in the DataFrame should match the order of the function arguments.
    - If there's any exception during the application of the function, it returns the exception message.
    """
    args = inspect.getfullargspec(fun).args
    if set(args) == set(df.columns):
        try:
            return list(map(fun, *df.values.T))
        except Exception as e:
            return str(e)
    else:
        return "NOT match col names and fun arguments!"
