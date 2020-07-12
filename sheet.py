from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from osrsbox import items_api
from datetime import datetime

items = items_api.load()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1WDrrRJpJFC3Y2FJh1DF6182Ep2PF6HLlSanx1ei7-Jg"

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

service = build("sheets", "v4", credentials=creds)


def make_body(*, range, id, name, bid, offer):
    now = datetime.now()
    return {
        "range": range,
        "majorDimension": "ROWS",
        "values": [[id, name, bid, offer, now.strftime("%H:%M:%S") ]],
    }


def update(*, id, bid, offer):
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range="SHEET1!A1:A50")
        .execute()
    )

    name = items.lookup_by_item_id(id).name
    row_idx = -1
    values = result.get("values")
    if values:
        for idx, row in enumerate(values):
            try:
                row = int(row[0])
                if id == row:
                    row_idx = idx
                    break
            except:
                pass

    if row_idx == -1:
        range = "SHEET1!A:E"
    else:
        range = "SHEET1!A{}:E{}".format(row_idx + 1, row_idx + 1)
    body = make_body(range=range, id=id, name=name, bid=bid, offer=offer)

    if row_idx == -1:
        result = (
            sheet.values()
            .append(
                spreadsheetId=SPREADSHEET_ID,
                range=range,
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body=body,
            )
            .execute()
        )
    else:
        result = (
            sheet.values()
            .update(
                spreadsheetId=SPREADSHEET_ID,
                range=range,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )

if __name__ == "__main__":
    update(id=1511, bid=234, offer=234)
    update(id=2, bid=234, offer=234)
