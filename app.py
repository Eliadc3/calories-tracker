from flask import Flask, render_template, request
from parser import load_food_db, parse_meal_line, FOOD_SINGULAR_MAP
from sheets_writer import append_row_to_sheet, get_all_rows
from datetime import datetime, timedelta
import pytz


israel = pytz.timezone("Asia/Jerusalem")
now = datetime.now(israel)

# יבוא כתיבה ל־Google Sheets
app = Flask(__name__)  # יוצרים אובייקט של אפליקציה

# טוען את טבלת המזון
food_df = load_food_db()

@app.route("/", methods=["GET", "POST"])
def index():
  results = None
  input_text = ""

# אם המשתמש שלח טופס
  if request.method == "POST":
    input_text = request.form["food_input"]
    # פונקציה שמקבלת שורה של מזון ומחזירה את הנתונים המחושבים
    results = parse_meal_line(food_df, input_text, FOOD_SINGULAR_MAP)

    # 🔹 שולח את הנתונים ל־Google Sheets
  if results:
    try:
        for row in results:
            if row["שם"] != "סה״כ":
                sheet_row = {
            "תאריך": now,
            "שם": row["מזון"],
            "כמות": row["כמות"],
            "יחידות": row["יחידה"],
            "קלוריות": row["קלוריות"],
            "גרם חלבון": row["חלבון"]
        }
                append_row_to_sheet(sheet_row)  # שומר כל רכיב בנפרד
        print("✅ Meal data appended to Google Sheets.")
    except Exception as e:
        print(f"❌ Error appending meal to Google Sheets: {e}")            
   # 🔹 שולח את התוצאה לדף HTML
  return render_template("index.html", results=results, input_text=input_text)

@app.route("/history")
def history():
    filter_option = request.args.get("filter", "All")
    filter_options = ["All", "Today", "Yesterday", "Last 7 Days", "Last 30 Days"]

    rows = get_all_rows()

    for row in rows:
        try:
            row["תאריך"] = datetime.strptime(row["תאריך"], "%d/%m/%Y %H:%M")
        except:
            row["תאריך"] = None

    
    if filter_option == "Today":
        rows = [r for r in rows if r["תאריך"] and r["תאריך"].date() == now.date()]
    elif filter_option == "Yesterday":
        rows = [r for r in rows if r["תאריך"] and r["תאריך"].date() == (now - timedelta(days=1)).date()]
    elif filter_option == "Last 7 Days":
        rows = [r for r in rows if r["תאריך"] and (now - r["תאריך"]).days < 7]
    elif filter_option == "Last 30 Days":
        rows = [r for r in rows if r["תאריך"] and (now - r["תאריך"]).days < 30]

    rows = sorted(rows, key=lambda r: r["תאריך"] or datetime.min, reverse=True)

    return render_template("history.html", rows=rows, filter_options=filter_options, filter_option=filter_option)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)