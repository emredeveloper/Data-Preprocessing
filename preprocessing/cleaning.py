"""
Basic data cleaning operations for common preprocessing tasks.
"""
import pandas as pd
import numpy as np
from typing import List, Union, Dict, Optional

def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None, keep: str = 'first') -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame.
    
    Args:
        df: Input DataFrame
        subset: Column names to consider for identifying duplicates
        keep: 'first', 'last', or False to indicate which duplicates to keep
        
    Returns:
        DataFrame with duplicates removed
    """
    return df.drop_duplicates(subset=subset, keep=keep)

def fill_missing_values(df: pd.DataFrame, 
                       strategy: Dict[str, Union[str, Dict[str, float]]] = None) -> pd.DataFrame:
    """
    Fill missing values using various strategies.
    
    Args:
        df: Input DataFrame
        strategy: Dict mapping column names to filling strategy
                 ('mean', 'median', 'mode', 'constant', or a custom value)
    
    Returns:
        DataFrame with missing values filled
    """
    df_copy = df.copy()
    
    if strategy is None:
        return df_copy
        
    for col, method in strategy.items():
        if col not in df_copy.columns:
            continue
            
        if method == 'mean':
            if pd.api.types.is_numeric_dtype(df_copy[col]):
                df_copy[col] = df_copy[col].fillna(df_copy[col].mean())
        elif method == 'median':
            if pd.api.types.is_numeric_dtype(df_copy[col]):
                df_copy[col] = df_copy[col].fillna(df_copy[col].median())
        elif method == 'mode':
            df_copy[col] = df_copy[col].fillna(df_copy[col].mode()[0])
        elif method == 'ffill':
            df_copy[col] = df_copy[col].ffill()
        elif method == 'bfill':
            df_copy[col] = df_copy[col].bfill()
        elif isinstance(method, (int, float, str)):
            df_copy[col] = df_copy[col].fillna(method)
    
    return df_copy

def remove_outliers(df: pd.DataFrame, 
                   columns: List[str], 
                   method: str = 'iqr', 
                   threshold: float = 1.5) -> pd.DataFrame:
    """
    Remove outliers from numerical columns.
    
    Args:
        df: Input DataFrame
        columns: List of numerical columns to check for outliers
        method: 'iqr' for IQR method, 'zscore' for Z-score method
        threshold: Threshold value (1.5 for IQR, typically 3 for Z-score)
    
    Returns:
        DataFrame with outliers removed
    """
    df_copy = df.copy()
    
    for col in columns:
        if not pd.api.types.is_numeric_dtype(df_copy[col]):
            continue
            
        if method == 'iqr':
            Q1 = df_copy[col].quantile(0.25)
            Q3 = df_copy[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df_copy = df_copy[(df_copy[col] >= lower_bound) & (df_copy[col] <= upper_bound)]
            
        elif method == 'zscore':
            from scipy import stats
            z_scores = np.abs(stats.zscore(df_copy[col]))
            df_copy = df_copy[z_scores < threshold]
    
    return df_copy

def format_dates(df: pd.DataFrame, 
                date_columns: List[str], 
                format: Optional[str] = None) -> pd.DataFrame:
    """
    Convert string columns to datetime.
    
    Args:
        df: Input DataFrame
        date_columns: List of columns to convert
        format: Date format string (e.g., '%Y-%m-%d')
    
    Returns:
        DataFrame with converted date columns
    """
    df_copy = df.copy()
    
    for col in date_columns:
        if col in df_copy.columns:
            df_copy[col] = pd.to_datetime(df_copy[col], format=format, errors='coerce')
    
    return df_copy