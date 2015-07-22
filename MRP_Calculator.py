'''
Functions with run MRP Logic
'''

import math
import pdb


def part_mrp(part_group):
    '''
    Takes part groups from MRP dataframe and runs MRP

    returns: Dataframe with Planned Receipt and Releases and error messages
    '''
    part_group.reset_index(level=0, drop=True, inplace=True)
    # Picking arbitrary values for now
    part_lt = 10
    order_qty = 10

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

        if net_requirement > 0:
            # Determine quantity needed for order
            po_receipt = math.ceil(net_requirement/order_qty) * order_qty
            
            part_week["POReceipt"] = po_receipt
            part_week["NR"] = net_requirement
            
            # Plan Order week
            receipt_week = i - part_lt
            if receipt_week <= 0:
                print("Exception message: PO Release required in the past")
                receipt_week = 0

            part_group.ix["PORelease", receipt_week] += po_receipt

        part_week["PA"] = previous_available + po_receipt - part_week["GR"]

    return part_group
