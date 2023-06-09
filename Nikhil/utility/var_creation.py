import numpy as np 
import pandas as pd


def churn_data(pivot_table):
    rows_with_consecutive_nan = []

    for _, row in pivot_table.iterrows():
        nan_count = 0
        for value in row:
            if pd.isna(value):
                nan_count += 1
                if nan_count >3 and nan_count<=12:
                    rows_with_consecutive_nan.append('Inactive_atleast_once')
                    break
                if nan_count>12:
                    rows_with_consecutive_nan.append('Churn')
                    break

            else:
                nan_count = 0
        else:
            rows_with_consecutive_nan.append(False)
    return rows_with_consecutive_nan

def count_zeros_before_first_nonzero(row):
    count = 0
    for value in row:
        if value == 0:
            count += 1
        else:
            break 
    return count