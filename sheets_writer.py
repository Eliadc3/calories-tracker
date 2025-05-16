import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz


# הגדרת איזור זמן של ישראל
def get_local_time():
  israel_tz = pytz.timezone('Asia/Jerusalem')
  return datetime.now(israel_tz).strftime("%d/%m/%Y %H:%M")

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
        food_data.get("תאריך", get_local_time()),
        food_data.get("שם",""),
        food_data.get("כמות", ""),
        food_data.get("יחידה", ""),
        food_data.get("קלוריות",""),
        food_data.get("חלבון",""), 
        food_data.get("סוג ארוחה","")    
    ]
  else:
    row = food_data
    print("📤 שולח שורה לגיליון:", row)
  sheet.append_row(row)

def get_all_rows():
  sheet = get_sheet()
  rows = sheet.get_all_values()
  headers = rows[0]
  data = [dict(zip(headers, row)) for row in rows[1:]]
  return data
