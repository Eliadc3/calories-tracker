import pandas as pd
import re
from utils.text_utils import load_plural_map ,load_unit_weights, parse_input_line, reverse_text
UNIT_WEIGHTS_GRAMS = load_unit_weights("data/unit_weights.csv")
FOOD_SINGULAR_MAP = load_plural_map("data/food_singular_map.csv")
#
UNIT_SINGULAR_MAP = {
    k.strip(): v.strip() 
    for k, v in load_plural_map("data/unit_singular_map.csv").items()
}


# טוען את קובץ המזון food_db.csv
def load_food_db():   
    food_df = pd.read_csv("data/food_db.csv")
    return food_df


# חישבו את הנתונים של השורה
def calculate_row_data(row, quantity):
    return {
        "name": row["שם"],
        "unit": row["יחידה"],
        "quantity": quantity,
        "calories": float(row["קלוריות"]) * quantity,
        "protein": float(row["חלבון"]) * quantity
    }


# פונקציה שמקבלת שורה של מזון ומחזירה את הנתונים המחושבים
def parse_line(food_df, food_input, plural_map):
    parsed = parse_input_line(food_input)
    food_name = plural_map.get(parsed["name"].strip(), parsed["name"].strip())
    print("🔍 מחרוזת לחיפוש:", repr(food_name))

    quantity = parsed["quantity"]
    input_unit = parsed["unit"]

    print(f"🧪 input_unit לפני המרה: {input_unit}")
    # ✅ המרת יחידת מידה מרבים ליחיד
    if input_unit:
        input_unit = UNIT_SINGULAR_MAP.get(input_unit.strip(), input_unit.strip())
        print(f"✅ input_unit אחרי המרה: {input_unit}")

    
    matches = food_df[food_df["שם"].str.strip().str.contains(food_name, case=False, na=False)]
    if matches.empty:
        print(reverse_text(f" לא נמצא מזון בשם: ❌ '{food_name}'"))
        return

    row = matches.iloc[0]
    db_unit = row["יחידה"].strip().replace('"', '').replace("‏", "").replace(" ", " ")

    final_quantity = quantity  # כברירת מחדל

    # חישוב לפי התאמה מדויקת של יחידת מידה כמו "100 גרם"
    if input_unit and db_unit.endswith(input_unit):
        match = re.search(r"(\d+(?:\.\d+)?)\s*" + re.escape(input_unit), db_unit)
        if match:
            base_amount = float(match.group(1))
            final_quantity = quantity / base_amount
            print(f"✅ יחס חישוב ישיר לפי {input_unit}: {quantity} / {base_amount} = {final_quantity:.2f}")
        else:
            print(f"⚠️ לא ניתן לחשב לפי {input_unit} – יחידת הבסיס היא: '{db_unit}'")

    # אם היחידה קיימת בטבלת ההמרות – נחשב לפי גרמים
    elif input_unit in UNIT_WEIGHTS_GRAMS:
        base_amount = UNIT_WEIGHTS_GRAMS[input_unit]
        print(f"ℹ️ בוצע חישוב לפי יחידת ברירת מחדל: {base_amount} גרם ל-{input_unit}")
        if db_unit.endswith("גרם"):
            match = re.search(r"(\d+(?:\.\d+)?)\s*גרם", db_unit)
            if match:
                unit_grams = float(match.group(1))
                final_quantity = (quantity * base_amount) / unit_grams
                print(f"✅ יחס לפי טבלת יחידות: {quantity} x {base_amount} / {unit_grams} = {final_quantity:.2f}")
        else:
            print(f"⚠️ לא ניתן להמיר {input_unit} ל־{db_unit}")


    data = calculate_row_data(row, final_quantity)
    from display import print_calculated_data
    print_calculated_data(data)
    return data