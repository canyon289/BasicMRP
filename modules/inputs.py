'''
Reads and formats all inputs for Material Requirements Planning
'''

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import pdb
import pandas as pd
from datetime import date


class google_docs_input:
    '''
    Authorizes with Google Docs and contains methods to return inventory,
    gross requirements and lead time dataframes

    returns : object with formatted dataframes
    '''

    def __init__(self, json_file=None, sheets_name=None):

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
       Run methods which read Google Sheets and
       return formatted dataframes as attributes

       returns: self
       '''

        self.sheets_item_attribute()
        self.sheets_read_gr()
        self.sheets_read_inventory()
        self.sheets_read_scheduled_receipts()
        self.sheets_read_scheduled_receipts()
        return self

    def _read_sheet(self, sheet_name, input_type=None, date_col=None, format=True):
        '''
        Reads google sheets and returns formatted df
        '''

        sheet = self.spreadsheet.worksheet(sheet_name)
        values = sheet.get_all_records()
        df = pd.DataFrame(values)

        # Skip formatting if attribute df e.g. BOM or Item Attribute values
        if format:
            assert input_type in ["GR", "SR", "PA", "NR"]
            df = self.format_dataframe(df, input_type, date_col)

        else:
            df = df.set_index("Part Number")

        return df

    def format_dataframe(self, input_df, input_type, date_col=None):
        '''
        Takes inputs for various dataframes and returns correct dataframe

        returns: Formatted dataframe ready for updating MRP table
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
        
    def explode_requirements(self):
        '''
        Using Top Level demand and BOM explodes the requirements for the individual items
        returns : Exploded Dataframe of dated demand
        '''

    def sheets_read_bom(self):
        '''
        Read BOM Spreadsheet of Google Docss
        '''
        self.bom_df = self._read_sheet("BOM", format=False)
        return self.bom_df

    def sheets_read_inventory(self):
        '''
        Read Inventory Spreadsheet of Google docs
        '''
        self.inventory_df = self._read_sheet("Inventory", "PA")
        return self.inventory_df

    def sheets_read_gr(self):
        '''
        Read Gross Requirements Spreadsheet of Google docs
        '''

        toplevel_gr = self.spreadsheet.worksheet("Gross Requirements").get_all_values()
        headers = toplevel_gr.pop(0)
        bom = self.sheets_read_bom()
        
        exploded_req = pd.DataFrame()
    
        for row in toplevel_gr:
            row_dict= dict(zip(headers,row))
            exploded_bom = bom * int(row_dict["Demand"])
            exploded_bom["Due Date"] = row_dict["Date Needed"]
            exploded_req= exploded_req.append(exploded_bom)
            
        exploded_req.reset_index(inplace = True)
        self.gr_df = self.format_dataframe(exploded_req, "GR", "Due Date")
        return self.gr_df

    def sheets_read_scheduled_receipts(self):
        '''
        Read Scheduled Receipts Spreadsheet of Google docs
        '''
        self.sr_df = self._read_sheet("Scheduled Receipts", "SR", "Date")
        return self.sr_df

    def sheets_item_attribute(self):
        '''
        Read Item Attributes Spreadsheet of Google docs. Item Attributes aren't parsed
        '''
        self.item_attr_df = self._read_sheet("Item Attributes", format=False)
        return self.item_attr_df


if __name__ == "__main__":
    io = google_docs_input()