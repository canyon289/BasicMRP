'''
Reads in demand from Excel using Pandas
'''
import pd
    
    
def read_demand(filename):
    '''
    Reads demand from Excel
    
    Returns: MultiIndex dataframe indexed on Part Number and Datebin
    '''
    filename = "MRP_Inputs.xlsx"
    df = pd.read_excel(filename, index_col = "Ship Date")
    max_date = max(df.index)
    df = df.to_period("W-SUN").reset_index().groupby(["Part Number", "Ship Date"]).sum()
    df["GR"] = "GR"
    df = df.set_index("GR", append=True)
    gr_df = df.unstack(level = 1)
    
    return max_date, gr_df