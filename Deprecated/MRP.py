'''
Deprecated 7-25-15
All MRP functions now reside in MRP Class
'''

# Placeholder item list and columns
item_list = ["C", "D"]
planning_horizon = list(range(6))
planning_horizon = pd.date_range(date.today(), periods = 6, freq = "W-SUN").to_period("W-SUN")

index_names = ["PN", "MRP_row"]

def generate_inventory_df():
    '''
    Creates Inventory dataframes

    returns: Current Inventory dataframe
    '''

    # Placeholder values
    inventory_values = [10, 0]

    inventory_index = pd.MultiIndex.from_product([item_list, ["PA"]], names=index_names)
    inventory_df = pd.DataFrame(inventory_values, index=inventory_index, columns=[planning_horizon[0]])

    return inventory_df



def generate_mrp_df():
    '''
    Creates an MRP Dataframe

    returns: MRP dataframe with current inventory, scheduled receipts, and gross demand
    '''

    mrp_rows = ["Gross Requirements", "Scheduled Receipts", "Projected Available",
                "Net Requirements", "Planned Order Receipt", "Planned Order Release"]

    # Shortened names for testing
    mrp_rows = ["GR", "SR", "PA",
                "NR", "POReceipt", "PORelease"]

    mrp_index = pd.MultiIndex.from_product([item_list, mrp_rows], names=index_names)
    mrp_df = pd.DataFrame(index=mrp_index, columns=planning_horizon).fillna(0)

    return mrp_df