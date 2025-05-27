from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from parser import load_food_db, parse_meal_line, FOOD_SINGULAR_MAP
from sheets_writer import append_row_to_sheet, get_all_rows, get_local_time
from food_detector import detect_food
from utils.translation_utils import load_translation_map, translate_items
from datetime import datetime, timedelta
import pytz
import os

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# יבוא כתיבה ל־Google Sheets
app = Flask(__name__)  # יוצרים אובייקט של אפליקציה
app.config["UPLOAD_FOLDER"] = "static/uploads"

# טוען את טבלת המזון
food_df = load_food_db()
translation_map = load_translation_map("data/food_translation_map.csv")

def get_meal_label(is_snack:bool, num_items: int, total_calories: float) -> str:
    israel = pytz.timezone("Asia/Jerusalem")
    hour = datetime.now(israel).hour

    if is_snack:
        return "נשנוש"
    if num_items <= 1 and total_calories <= 200:
        return "נשנוש"
    if 0 <= hour < 5:
        return "לילה"
    elif 5 <= hour < 11:
        return "בוקר"
    elif 11 <= hour < 18:
        return "צהריים"
    elif 18 <= hour < 22:
        return "ערב"
    elif 22 <= hour < 24:
        return "לילה"
    return "נשנוש"


@app.route("/", methods=["GET", "POST"])
def index():
  results = None
  input_text = ""

  if request.method == "POST":

    # אם המשתמש שלח תמונה
    if "image_input" in request.files:
        image = request.files["image_input"]
        if image and image.filename != "":
            path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(path)

            english_items = detect_food(path)
            hebrew_items = translate_items(english_items, translation_map)

            return render_template("confirm_foods.html", detected=hebrew_items, image_path=path)

# אם המשתמש שלח טקסט
    input_text = request.form["food_input"]
    # פונקציה שמקבלת שורה של מזון ומחזירה את הנתונים המחושבים
    results = parse_meal_line(food_df, input_text, FOOD_SINGULAR_MAP)

        # קלט תאריך ושעה ידני (אם סופק)
    manual_dt_str = request.form.get("manual_datetime", "").strip()
    is_snack = "is_snack" in request.form

    if manual_dt_str:
        parsed_dt = datetime.strptime(manual_dt_str, "%Y-%m-%dT%H:%M")
        date_str = parsed_dt.strftime("%d/%m/%Y %H:%M")
    else:
        from sheets_writer import get_local_time
        date_str = get_local_time()


    # 🔹 שולח את הנתונים ל־Google Sheets
  if results:
    try:
        num_items = len([r for r in results if r["שם"] != "סה״כ"])
        summary = next((r for r in results if r["שם"] == "סה״כ"), None)
        
        total_calories = summary["קלוריות"] if summary else 0
        meal_type = get_meal_label(is_snack, num_items, total_calories)

        for row in results:
            if row["שם"] != "סה״כ":
                sheet_row = {
                  "תאריך": date_str,
                  "שם": row["שם"],
                  "כמות": row["כמות"],
                  "יחידה": row["יחידה"],
                  "קלוריות": row["קלוריות"],
                  "חלבון": row["חלבון"],
                  "סוג ארוחה": meal_type
                }
                append_row_to_sheet(sheet_row)  # שומר כל רכיב בנפרד
        print("✅ Meal data appended to Google Sheets.")
    except Exception as e:
        print(f"❌ Error appending meal to Google Sheets: {e}")            
   # 🔹 שולח את התוצאה לדף HTML
  return render_template("index.html", results=results, input_text=input_text)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if "image" not in request.files:
            return "❌ לא נבחר קובץ"
        file = request.files["image"]
        
        if file.filename == "":
            return "❌ שם הקובץ ריק"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            
            # זיהוי המאכלים מהתמונה
            detected_items = detect_food(filepath)
            return render_template("confirm_foods.html", image_path=filepath, detected=detected_items)
        
    return render_template("upload.html")


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

    israel = pytz.timezone("Asia/Jerusalem")
    now = datetime.now(israel)
    
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