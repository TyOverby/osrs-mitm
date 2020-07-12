from __future__ import print_function
import json
from mitmproxy import ctx
from mitmproxy import http
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from osrsbox import items_api
import sheet

#   items = items_api.load()


#   flag=False

#   # If modifying these scopes, delete the file token.pickle.
#   SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#   # The ID and range of a sample spreadsheet.
#   SAMPLE_SPREADSHEET_ID = '1WDrrRJpJFC3Y2FJh1DF6182Ep2PF6HLlSanx1ei7-Jg'

#   def main(data):
#       """Shows basic usage of the Sheets API.
#       Prints values from a sample spreadsheet.
#       """
#       creds = None
#       # The file token.pickle stores the user's access and refresh tokens, and is
#       # created automatically when the authorization flow completes for the first
#       # time.
#       if os.path.exists('token.pickle'):
#           with open('token.pickle', 'rb') as token:
#               creds = pickle.load(token)
#       # If there are no (valid) credentials available, let the user log in.
#       if not creds or not creds.valid:
#           if creds and creds.expired and creds.refresh_token:
#               creds.refresh(Request())
#           else:
#               flow = InstalledAppFlow.from_client_secrets_file(
#                   'credentials.json', SCOPES)
#               creds = flow.run_local_server(port=0)
#           # Save the credentials for the next run
#           with open('token.pickle', 'wb') as token:
#               pickle.dump(creds, token)

#       service = build('sheets', 'v4', credentials=creds)

#       # Call the Sheets API
#       sheet = service.spreadsheets()
#       parsed = json.loads(data)
#       out = {
#               "range": "SHEET1!A:A",
#                   "majorDimension": "ROWS",
#                   "values":[[
#                       data,
#                       parsed.get("buy"),
#                       parsed.get("cancel"),
#                       parsed.get("login"),
#                       parsed.get("itemId"),
#                       items.lookup_by_item_id(parsed.get("itemId")).name,
#                       parsed.get("qty"),
#                       parsed.get("dqty"),
#                       parsed.get("total"),
#                       parsed.get("spent"),
#                       parsed.get("dspent"),
#                       parsed.get("offer"),
#                       parsed.get("slot")
#                       ]]
#               }
#       result = sheet.values().append(
#               spreadsheetId=SAMPLE_SPREADSHEET_ID,
#               range='SHEET1!A:A',
#               valueInputOption='USER_ENTERED',
#               insertDataOption='INSERT_ROWS',
#               body=out).execute()


def response(flow: http.HTTPFlow):
    text = flow.request.get_text()
    parsed = json.loads(text)

    buy = parsed.get("buy")
    cancel = parsed.get("cancel")
    login = parsed.get("login")
    itemId = parsed.get("itemId")
    qty = parsed.get("qty")
    dqty = parsed.get("dqty")
    total = parsed.get("total")
    spent = parsed.get("spent")
    dspent = parsed.get("dspent")
    offer = parsed.get("offer")
    slot = parsed.get("slot")

    if qty > 0:
        if buy:
            sheet.update(id=itemId, bid=None, offer=spent)
        else:
            sheet.update(id=itemId, bid=spent, offer=None)
    ctx.log.info(text)
