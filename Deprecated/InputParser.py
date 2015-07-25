'''
Input functions for Google Docs and DataNitro with helper functions to bin dates
'''
import pandas as pd
from datetime import date
import ipdb


index_names = ["PN", "MRP_row"]


def df_parser(input_df, date_col, input_type):
    '''
    Takes inputs for various dataframes and returns correct dataframe
    
    returns: Properly mutliindexed dataframe ready for updating MRP table
    '''
    period_type = "W-SUN"
    input_df[date_col]  = pd.to_datetime(input_df[date_col])
    input_df.set_index(date_col, inplace=True)
    input_df = input_df.to_period(period_type).reset_index()
    input_df = input_df.groupby(by = ["Part Number"] + [date_col]).sum()
    input_df[input_type] = input_type
    input_df = input_df.set_index(input_type, append=True)
    input_df = input_df.unstack(level = 1)
    input_df.columns = input_df.columns.droplevel()
    
    return input_df
    
    
def test_gen_grossrequirements():
    '''
    Test function for generating gross requirements
    '''
    
    gr_values = [["C",20, date(2015, 7, 28)],["C",30, date(2015, 8, 30)], ["D",20, date(2015, 7, 29)]]
    columns = ["Part Number", "GR_int", "Week"]
    
    p = pd.DataFrame(gr_values, columns=columns)
    
    return df_parser(p, "Week", "GR")
    
df = test_gen_grossrequirements()


