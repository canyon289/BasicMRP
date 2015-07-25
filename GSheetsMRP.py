

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import pdb
import pandas as pd
from datetime import date


class google_docs_input:
    '''
    Authorizes with Google Docs and contains methods to return inventory, gross requirements
    and lead time dataframes

    returns : object with formatted dataframes
    '''

    def __init__(self, json_file = None, sheets_name = None):

        json_key = json.load(open('MRPTest-eda1f9edd61a.json'))
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'utf-8'), scope)
        gc = gspread.authorize(credentials)
        mrp_inputs = gc.open("MRP_Input")

        self.spreadsheet = mrp_inputs
        self.get_dataframes()
        return

    def get_dataframes(self):
        '''
        Gets dataframes from google sheets_item_attribute
        '''
        self.sheets_item_attribute()

        self.sheets_read_gr()
        self.sheets_read_inventory()

        # Haven't added scheduled receipts at the time
        # self.sheets_read_scheduled_receipts()
        return self

    def parse_dataframe(self, input_df, input_type, date_col=None):
        '''
        Takes inputs for various dataframes and returns correct dataframe

        returns: Properly mutliindexed dataframe ready for updating MRP table
        '''
        if date_col is None:
            date_col = "Date"
            input_df[date_col] = date.today()

        period_type = "W-SUN"

        # Bin values into date buckets
        input_df[date_col] = pd.to_datetime(input_df[date_col])
        input_df.set_index(date_col, inplace=True)
        input_df = input_df.to_period(period_type).reset_index()

        # Sum values and format dataframe
        input_df = input_df.groupby(by=["Part Number"] + [date_col]).sum()
        input_df[input_type] = input_type
        input_df = input_df.set_index(input_type, append=True)
        input_df = input_df.unstack(level=1)
        input_df.columns = input_df.columns.droplevel()

        return input_df

    def sheets_read_inventory(self):
        '''
        Read Inventory Spreadsheet of Google docs
        '''
        inventory_sheet = self.spreadsheet.worksheet("Inventory")
        values = inventory_sheet.get_all_records()
        inventory_df = pd.DataFrame(values)
        self.inventory_df = self.parse_dataframe(inventory_df, "PA")
        return inventory_df

    def sheets_read_gr(self):
        '''
        Read Gross Requirements Spreadsheet of Google docs
        '''
        gross_requirements = self.spreadsheet.worksheet("Gross Requirements")
        values = gross_requirements.get_all_records()
        gr_df = pd.DataFrame(values)
        self.gr_df = self.inventory_df = self.parse_dataframe(gr_df, "GR", "Date Needed")
        return gr_df

    def sheets_read_scheduled_receipts(self):
        '''
        Read Scheduled Receipts Spreadsheet of Google docs
        '''
        scheduled_receipts = self.spreadsheet.worksheet("Scheduled Receipts")
        values = scheduled_receipts.get_all_records()
        sr_df = pd.DataFrame(values)
        self.sr_df = sr_df
        return sr_df

    def sheets_item_attribute(self):
        '''
        Read Item Attributes Spreadsheet of Google docs
        '''
        item_attr = self.spreadsheet.worksheet("Item Attributes")
        values = item_attr.get_all_records()
        item_attr_df = pd.DataFrame(values)
        self.item_attr = item_attr
        return item_attr_df


class MRP:
    '''
    Reads input dataframes and calculates MRP
    '''

    def __init__(self, input_object):
        '''
        Read in input object if exists
        '''
        self.mrp_input = input_object
        self.gen_mrp_table()
            
        return

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
        item_list = ["C", "D"]
        planning_horizon = pd.date_range(date.today(), periods=6, freq="W-SUN").to_period("W-SUN")
        index_names = ["PN", "MRP_row"]

        mrp_index = pd.MultiIndex.from_product([item_list, mrp_rows], names=index_names)
        mrp_df = pd.DataFrame(index=mrp_index, columns=planning_horizon).fillna(0)

        self.mrp_table = mrp_df
        return self

    def update_mrp_table(self):
        '''
        updates mrp table with inputs
        '''

        self.mrp_table.update(self.mrp_input.inventory_df)
        self.mrp_table.update(self.mrp_input.gr_df)
        # Add Planned Receipts Later
        return

if __name__ == "__main__":
    i = google_docs_input('MRPTest-eda1f9edd61a.json', "MRP_Input")
    m = MRP(i).gen_mrp_table()