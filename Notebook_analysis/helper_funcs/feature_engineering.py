def split_df(df, train_idx, valid_idx, y_var):
    """
    Splits the dataframe into a test and training set based on the indexes and then 
    further splits based dependant and independant variables
    Parameters
    ----------
    df: DataFrame
        Dataframe to split
    train_idx: index or array like:
        Set of indexes for the training set
    valid_idx: index or array like:
        Set of indexes for the validation set
    y_var: String
        The dependant variable
        
    Return
    ----------
    X_train: DataFrame or Series
        The independant variables for the training set 
    y_train: Series
        The dependant variable for the training set
    X_valid: DataFrame or Series
        The independant variables for the validation set 
    y_valid: Series
        The dependant variable for the validation set
   
    """
    
    df_train = df.iloc[train_idx] 
    df_valid = df.iloc[valid_idx]
    
    X_train = df_train.drop(y_var,axis=1) 
    y_train = df_train[y_var]
    X_valid = df_valid.drop(y_var,axis=1) 
    y_valid = df_valid[y_var]
    
    return X_train, y_train, X_valid, y_valid