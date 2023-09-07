from typing import List
from urllib.request import urlopen
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

import googleapiclient.discovery
import functions_framework
import base64
import os
import json
import certifi
import ssl


FINANCE_MODELING_PREP_API_KEY = os.environ.get("FINANCE_MODELING_PREP_API_KEY", None)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def stock_retriever(cloud_event):
    '''
    Entry point for Google Cloud Function
    '''

    # Preparing to make a delegated API call
    # 1. Create a Credentials object from the service account's credentials
    creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)

    # Use the authorized Credentials object to call Google API by completing the following steps
    # 1. Build a service object for the API    
    gsheet_api = googleapiclient.discovery.build('sheets', 'v4', credentials=creds)

    stock_data = get_quote('AAPL')[0]
    header_row = list(stock_data.keys())
    content = list(stock_data.values())

    SPREADSHEET_ID = "1tEo3vshkEXQCPpAe5xAqF4BfQBFNIX5eMR79o2RlMZc"

    response_body = []
    # update header row
    result1 = update_values(gsheet_api, SPREADSHEET_ID, "Sheet1!1:1", "USER_ENTERED", header_row) 

    # append the table with latest stock data
    result2 = append_values(gsheet_api, SPREADSHEET_ID, "Sheet1", "USER_ENTERED", content) 

    response_body.append(result1)
    response_body.append(result2)

    # Print out the data from Pub/Sub, to prove that it worked
    print(base64.b64decode(cloud_event.data["message"]["data"]))

    return {'status': 200, 'body': response_body}

def get_quote(stock_symbol: str) -> List[object]:
    '''Get stock data for a given stock symbol

    Paramaters:
    stock_symbol (str): stock symbol of a company

    Returns:
    data (List[object]): Information about the stock
    '''

    context = ssl.create_default_context(cafile=certifi.where())
    url = f"https://financialmodelingprep.com/api/v3/quote/{stock_symbol}?apikey={FINANCE_MODELING_PREP_API_KEY}"
    response = urlopen(url, context=context)
    data = json.loads(response.read().decode('utf-8'))
    return data

def update_values(service, spreadsheet_id, range_name, value_input_option, _values):
    '''
    Write data into google sheet. This function is called to update the header row of the gsheet

    Parameters:
    service (object): a google sheet api service object
    spreadsheet_id (str): the spreadsheet id of the google sheet
    range_name (str): Range of cell in A1 notation
    value_input_option (str):  "RAW" or "USER_ENTERED"
    _values (List[str]): data to be inserted to the google sheet

    '''
    try:
        values = [
            _values
        ]

        body = {
            'values': values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as err:
        print(f"An error occurred: {err}")
        return err


def append_values(service, spreadsheet_id, range_name, value_input_option, _values):
    '''
    Append data into google sheet. This function is called to insert new row of stock data into the gsheet

    Parameters:
    service (object): a google sheet api service object
    spreadsheet_id (str): the spreadsheet id of the google sheet
    range_name (str): Range of cell in A1 notation
    value_input_option (str):  "RAW" or "USER_ENTERED"
    _values (List[str]): data to be inserted to the google sheet

    '''

    try:
        values = [
            _values
        ]

        body = {
            'values': values
        }

        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        

        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result
    
    except HttpError as err:
        print(f"An error occurred: {err}")
        return err
