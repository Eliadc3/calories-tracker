# התחברות ל־Google Sheets בעזרת gspread + JSON
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# הגדרת ההרשאות
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# טוען את הקובץ JSON שהעלית לפרויקט
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)

# יוצר חיבור ל־Google Sheets
client = gspread.authorize(creds)

# פותח את הגיליון לפי השם שנתת לו
sheet = client.open("CaloriesTrackerData").sheet1

# מדפיס את הערך בתא הראשון (בדיקה)
print(sheet.cell(1, 1).value)