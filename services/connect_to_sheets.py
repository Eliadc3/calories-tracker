# התחברות ל־Google Sheets בעזרת gspread + JSON
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet():
        
    # הגדרת ההרשאות
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # טוען את הקובץ JSON שהעלית לפרויקט
    creds_json = os.environ["GOOGLE_CREDENTIALS"]
    creds_dict = json.loads(creds_json)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    # יוצר חיבור ל־Google Sheets
    client = gspread.authorize(creds)

    # פותח את הגיליון לפי השם שנתת לו
    sheet = client.open("CaloriesTrackerData").sheet1
    print("📥 GOOGLE_CREDENTIALS loaded:", os.environ.get("GOOGLE_CREDENTIALS") is not None)
    # מדפיס את הערך בתא הראשון (בדיקה)
    print(sheet.cell(1, 1).value)