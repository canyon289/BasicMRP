'''
Basic MRP System that uses Pandas and a spreadsheet software as a interface
'''

import pandas as pd
import numpy as np
from datetime import date
import math
import pdb


def calc_mrp(mrp_object):
    '''
    Runs MRP Calculations by part number
    '''
    mrp_object.mrp_plan = mrp_object.mrp_table.groupby(level=0).apply(part_mrp, item_attr = mrp_object.inputs.item_attr_df)

    return mrp_object


def part_mrp(part_group, item_attr):
    '''
    Takes part groups from MRP dataframe and runs MRP

    returns: Dataframe with Planned Receipt and Releases and error messages
    '''
    # Remove part number index and get part number
    part_num = part_group.index.get_level_values(0)[0]
    part_group.reset_index(level=0, drop=True, inplace=True)

    # Get Item attributes
    part_lt = item_attr.loc[part_num, "Lead Time (Weeks)"]
    order_qty = item_attr.loc[part_num, "Order Quantity"]
    part_safety_lt = item_attr.loc[part_num, "Safety Lead Time (Weeks)"]
    part_safety_stock = item_attr.loc[part_num, "Safety Stock (Units)"]

    for i, week in enumerate(part_group.columns):
        # Skip Week 0 / Current week
        if i == 0:
            continue

        # Set weeks, projected inventory, and clear variables
        part_week = part_group.iloc[:, i]
        previous_available = part_group.ix["PA", i-1]
        po_receipt, net_requirement = (0, 0)

        if part_week["GR"] > 0:
            net_requirement = part_week["GR"] - part_week["SR"] - previous_available
        
        # Change integerer
        # pdb.set_trace()
        if (net_requirement - part_safety_stock) > 0:
            # Determine quantity needed for order
            po_receipt = math.ceil(net_requirement/order_qty) * order_qty

            part_week["POReceipt"] = po_receipt
            part_week["NR"] = net_requirement

            # Plan Order week
            receipt_week = i - part_lt - part_safety_lt
            if receipt_week <= 0:
                print("Exception message: PO Release required in the past")
                receipt_week = 0

            part_group.ix["PORelease", receipt_week] += po_receipt

        part_week["PA"] = previous_available + po_receipt + part_week["SR"]- part_week["GR"]

    return part_group
