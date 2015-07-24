'''
Deprecated Functions
'''
def generate_grossrequirements_df():
    '''
    Creates Inventory dataframes

    returns: Current Inventory dataframe
    
    Deprecated as simple function was developed
    '''
7
    # Placeholder values
    gr_values = [["C",20, date(2015, 7, 28)],["C",30, date(2015, 8, 30)], ["D",20, date(2015, 7, 29)]]
    columns = ["Part Number", "GR_int", "Week"]
    
    # df = df.to_period("W-SUN").reset_index().groupby(["Part Number", "Ship Date"]).sum()
    # df["GR"] = "GR"
    # df = df.set_index("GR", append=True)
    # gr_df = df.unstack(level = 1)

    # Convert to dataframe
    # Refactor this at a later point
    p = pd.DataFrame(gr_values, columns=columns)
    p["Week"]  = pd.to_datetime(p["Week"])
    p.set_index("Week", inplace=True)
    p = p.to_period("W-SUN").reset_index().groupby(["Part Number", "Week"]).sum()
    p["GR"] = "GR"
    p = p.set_index("GR", append=True)
    p = p.unstack(level = 1)
    p.columns = p.columns.droplevel()

    return p