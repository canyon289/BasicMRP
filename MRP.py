import inputs
import requirements_calc
import pandas as pd
from datetime import date
import pdb


class mrp:
    '''
    Reads input dataframes and calculates MRP
    '''

    def __init__(self, input_object):
        '''
        Read in input object if exists
        '''
        self.inputs = input_object
        self.gen_mrp_table()

        return

    def gen_item_list(self):
        '''
        Gets item list from BOM df and verifies against Item Attribute
        Refactor this at a future date
        '''
        items = self.inputs.bom_df.index
        assert items.isin(self.inputs.item_attr_df.index).all(),
                "Ensure all items have attributes"

        return items

    def gen_mrp_table(self):
        '''
        Creates MRP Table
        '''
        mrp_rows = ["Gross Requirements", "Scheduled Receipts", "Projected Available",
                    "Net Requirements", "Planned Order Receipt", "Planned Order Release"]

        # Shortened names for testing
        mrp_rows = ["GR", "SR", "PA",
                    "NR", "POReceipt", "PORelease"]

        # Clean up later
        index_names = ["PN", "MRP_row"]
        item_list = self.gen_item_list()
        planning_horizon = pd.date_range(date.today(), periods=7, freq="W-SUN").to_period("W-SUN")

        mrp_index = pd.MultiIndex.from_product([item_list, mrp_rows], names=index_names)
        mrp_df = pd.DataFrame(index=mrp_index, columns=planning_horizon).fillna(0)

        self.mrp_table = mrp_df

        return self

    def update_mrp_table(self):
        '''
        updates mrp table with inputs
        '''

        self.mrp_table.update(self.inputs.inventory_df)
        self.mrp_table.update(self.inputs.gr_df)
        # Add Planned Receipts Later

        return self

if __name__ == "__main__":
    i = inputs.google_docs_input('MRPTest-eda1f9edd61a.json', "MRP_Input")
    m = mrp(i).gen_mrp_table()
