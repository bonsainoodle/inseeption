import pandas as pd
import numpy as np


def init_new_df(df, cols):
    """
    Create a new DataFrame object with the wanted columns inside

            Parameters:
                    df (pd.DataFrame): Previously downloaded csv that was converted to a DataFrame object
                    cols (List[str]): List of columns you want to keep

            Returns:
                    df_to_return (pd.DataFrame): New DataFrame object that contains only wanted columns
    """
    
    df_to_return = pd.DataFrame()

    df_to_return["IRIS"] = df["IRIS"] # Copy IRIS column to the new df since it will be our primary key
    
    for col in cols:
        df_to_return[col] = df[col] # Copy every wanted column to the new df
    
    return df_to_return


def complete_new_df(df, lenght, prefix, start=0, last_is_total_minus_sum=False):
    """
    Create a new DataFrame object that contains new columns that are the result of previous ones calculations

            Parameters:
                    df (pd.DataFrame): Previously initialised DataFrame object that contains only wanted columns + "IRIS" column
                    lenght (int): Number of columns you want at the end
                    prefix (str): Prefix of the columns you want at the end (if prefix="hello" & lenght=2, columns=["hello0", "hello1", "hello2"])
                    start (int): Where should the columns suffix start (if prefix="hello" & lenght=3 & start=1, columns=["hello1", "hello2", "hello3"])
                    last_is_total_minus_sum (bool): Should the last column be the result of first_col - sum(all others)

            Returns:
                    df_to_return (pd.DataFrame): New DataFrame object that contains "IRIS" column + newly created columns
    """
    
    cols = []
    
    x_return = pd.DataFrame()
    x_df = pd.DataFrame()
    
    df_to_return_debug = pd.DataFrame({df.columns[0]: []})
    df_to_return_debug[df.columns[0]] = df[df.columns[0]] # Copy IRIS column to df_to_return_debug
    
    for i in range(start, lenght + start):
        cols.append(str(prefix) + str(i)) # Create the new cols names
    
    # If first column shouldn't be copied
    if (len(df.columns) - 1) != lenght or last_is_total_minus_sum:
        df_to_return_debug[df.columns[1]] = df[df.columns[1]]
        
        if not last_is_total_minus_sum:
            for i in range(len(cols)):
                index = i + 2
                df_to_return_debug[cols[i]] = df.iloc[:, index] / df.iloc[:, 1] 
            x_return = df_to_return_debug.drop(df_to_return_debug.columns[0], axis=1) # Drop IRIS column
            x_df = df.drop(df.columns[0], axis=1) # Drop IRIS column
            x_df = x_df.drop(x_df.columns[0], axis=1) # Drop first column for later calculation (sum_others should be equal to this column)
            
        else:
            sum_cols = pd.Series(0, np.arange(len(df.iloc[:, 1])))
            for i in range(len(cols) - 1):
                index = i + 2
                sum_cols += df.iloc[:, index]
                df_to_return_debug[cols[i]] = df.iloc[:, index] / df.iloc[:, 1] 
            df_to_return_debug[cols[-1]] = df.iloc[:, 1] - sum_cols
            
            x_return = df_to_return_debug.drop(df_to_return_debug.columns[0], axis=1) # Drop IRIS column
            x_df = df.drop(df.columns[0], axis=1) # Drop IRIS column
            x_df = x_df.drop(x_df.columns[0], axis=1) # Drop first column for later calculation (sum_others should be equal to this column)
      
    # If first column should be included  
    elif (len(df.columns) - 1) == lenght:
        df_to_return_debug[cols[0]] = df[df.columns[1]]
        cols.remove(cols[0])
        for i in range(len(cols)):
            index = i + 2
            df_to_return_debug[cols[i]] = df.iloc[:, index] / df.iloc[:, 1]
        x_return = df_to_return_debug.drop(df_to_return_debug.columns[0], axis=1) # Drop IRIS column
        x_return = x_return.drop(x_return.columns[0], axis=1) # Drop first column since it won't be used late on
        x_df = df.drop(df.columns[0], axis=1) # Drop IRIS column
        x_df = x_df.drop(x_df.columns[0], axis=1) # Drop first column for later calculation (sum_others should be equal to this column)
    
    df_to_return_debug["sum_others"] = x_df.sum(axis = 1, skipna = True) # Calculate sum of all column except IRIS and the first one  (this sum should be equal to the first column (not IRIS))
    
    # Calculate sum of all probs (it should be equal to 1)
    df_to_return_debug["sum"] = 0
    if last_is_total_minus_sum:
        cols.remove(cols[-1])
    for col in cols:
        df_to_return_debug["sum"] += x_return[col]
    
    # Calculate with an error tolerance if there are outliers 
    error_tolerance = 0.1
               
    if abs(min(df_to_return_debug["sum"]) - 1) >= error_tolerance or abs(max(df_to_return_debug["sum"]) - 1) >= error_tolerance: 
        print("Sum of columns not equals to 1 for prefix: %s!" % prefix) # Should be an exception   
    
    df_to_return = df_to_return_debug
    df_to_return.drop(df_to_return.columns[[1, len(df_to_return.columns) - 2, len(df_to_return.columns) - 1]], axis=1, inplace=True) # Only keep IRIS column and used columns
    df_to_return.replace([np.inf, -np.inf], np.nan, inplace=True) # Replace inf values by none values
    df_to_return = df_to_return.rename(columns={"IRIS": "COD_IRIS"})
    
    return df_to_return


def complete_new_df_debug(df, lenght, prefix, start=0, last_is_total_minus_sum=False):
    """
    Same function as complete_new_df except it returns also a debug column

            Returns:
                    df_to_return_debug (pd.DataFrame): New DataFrame object that contains "IRIS" column + newly created columns + "sum" column that is the sum of all columns except the "IRIS" one (it should be around 1 except for outliers)
    """
    
    cols = []
    
    x_return = pd.DataFrame()
    x_df = pd.DataFrame()
    
    df_to_return_debug = pd.DataFrame({df.columns[0]: []})
    df_to_return_debug[df.columns[0]] = df[df.columns[0]] # Copy IRIS column to df_to_return_debug
    
    for i in range(start, lenght + start):
        cols.append(str(prefix) + str(i)) # Create the new cols name 
    
    # If first column shouldn't be copied
    if (len(df.columns) - 1) != lenght or last_is_total_minus_sum:
        df_to_return_debug[df.columns[1]] = df[df.columns[1]]
        
        if not last_is_total_minus_sum:
            for i in range(len(cols)):
                index = i + 2
                df_to_return_debug[cols[i]] = df.iloc[:, index] / df.iloc[:, 1] 
            x_return = df_to_return_debug.drop(df_to_return_debug.columns[0], axis=1) # Drop IRIS column
            x_df = df.drop(df.columns[0], axis=1) # Drop IRIS column
            x_df = x_df.drop(x_df.columns[0], axis=1) # Drop first column for later calculation (sum_others should be equal to this column)
            
        else:
            sum_cols = pd.Series(0, np.arange(len(df.iloc[:, 1])))
            for i in range(len(cols) - 1):
                index = i + 2
                sum_cols += df.iloc[:, index]
                df_to_return_debug[cols[i]] = df.iloc[:, index] / df.iloc[:, 1] 
            df_to_return_debug[cols[-1]] = df.iloc[:, 1] - sum_cols
            
            x_return = df_to_return_debug.drop(df_to_return_debug.columns[0], axis=1) # Drop IRIS column
            x_df = df.drop(df.columns[0], axis=1) # Drop IRIS column
            x_df = x_df.drop(x_df.columns[0], axis=1) # Drop first column for later calculation (sum_others should be equal to this column)
      
    # If first column should be included  
    elif (len(df.columns) - 1) == lenght:
        df_to_return_debug[cols[0]] = df[df.columns[1]]
        cols.remove(cols[0])
        for i in range(len(cols)):
            index = i + 2
            df_to_return_debug[cols[i]] = df.iloc[:, index] / df.iloc[:, 1]
        x_return = df_to_return_debug.drop(df_to_return_debug.columns[0], axis=1) # Drop IRIS column
        x_return = x_return.drop(x_return.columns[0], axis=1) # Drop first column since it won't be used late on
        x_df = df.drop(df.columns[0], axis=1) # Drop IRIS column
        x_df = x_df.drop(x_df.columns[0], axis=1) # Drop first column for later calculation (sum_others should be equal to this column)
    
    df_to_return_debug["sum_others"] = x_df.sum(axis = 1, skipna = True) # Calculate sum of all column except IRIS and the first one  (this sum should be equal to the first column (not IRIS))
    
    # Calculate sum of all probs (it should be equal to 1)
    df_to_return_debug["sum"] = 0
    for col in cols:
        df_to_return_debug["sum"] += x_return[col]
        
    return df_to_return_debug