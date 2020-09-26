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
