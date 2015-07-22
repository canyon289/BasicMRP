import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('MRPTest-eda1f9edd61a.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'utf-8'), scope)

gc = gspread.authorize(credentials)