'''
Basic MRP System that uses Pandas and a spreadsheet software as a interface
'''

import pandas as pd
import numpy as np


# Testing MRP dataframes

# Placeholder item list and columns
item_list = ["C", "D"]
planning_horizon = list(range(6))
index_names = ["PN", "MRP_row"]

def generate_inventory_df():
    '''
    Creates Inventory dataframes

    returns: Current Inventory dataframe
    '''

    # Placeholder values
    inventory_values = [10, 0]

    inventory_index = pd.MultiIndex.from_product([item_list, ["PA"]], names=index_names)
    inventory_df = pd.DataFrame(inventory_values, index=inventory_index, columns=[0])

    return inventory_df


def generate_grossrequirements_df():
    '''
    Creates Inventory dataframes

    returns: Current Inventory dataframe
    '''

    # Placeholder values
    gr_values = [["C",20, 3],["C",30, 4], ["D",20, 3]]
    columns = ["PN", "GR_int", "Week"]

    # Convert to dataframe
    # Refactor this at a later point
    p = pd.DataFrame(gr_values, columns=columns)
    p["MRP_row"] = "GR"
    p = p.set_index(["PN", "MRP_row", "Week"], ).unstack()
    p.columns = p.columns.droplevel()

    return p


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


d = generate_mrp_df()
i = generate_inventory_df()
g = generate_grossrequirements_df()