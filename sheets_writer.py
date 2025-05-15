import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# יוצרים חיבור ל־ Google Sheets
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = os.environ["GOOGLE_CREDENTIALS"]
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("CaloriesTrackerData").sheet1
    return sheet

# פונקציה שמוסיפה שורה
def append_row_to_sheet(food_data):
  sheet = get_sheet()
  if isinstance(food_data, dict):
    row = [
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        food_data.get("name",""),
        food_data.get("quantity", ""),
        food_data.get("unit", ""),
        food_data.get("calories",""),
        food_data.get("protein",""),     
    ]
  else:
    row = food_data
  sheet.append_row(row)

def get_all_rows():
  sheet = get_sheet()
  rows = sheet.get_all_values()
  headers = rows[0]
  data = [dict(zip(headers, row)) for row in rows[1:]]
  return data
