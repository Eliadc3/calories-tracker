import re
from utils.text_utils import reverse_text

# מדפיס שורה של מזון עם כמות מחושבת
def print_calculated_data(data):
    name = data["name"][::-1]  # שם המזון הפוך
    quantity = data["quantity"]
    
    unit_raw = data["unit"]
    # מזהה "מספר + מילה" ומרכיב יחידה בצורה הפוכה רק למילה
    match = re.match(r"^(\d+(?:\.\d+)?)\s+(.+)$", unit_raw)
    if match:
        number = float(match.group(1))
        word = match.group(2)[::-1]  # המילה בלבד מתהפכת
        unit = f"{word} {number}"  # נשמר: 100 םרג
    else:
        unit = unit_raw[::-1]  # לדוגמה: הדיחי → יכיד

    unit_display = f"({unit})"  # בונה סוגריים תקינים
    calories = f"{data['calories']:.1f}"  # מספר — נשמר
    protein = f"{data['protein']:.1f}"  # מספר — נשמר

    
    line = f"{'ןובלח'} {'םרג'} {protein} ,{'תוירולק'} {calories} :{quantity} x {unit_display} {name}"
    print(line)

# מדפיס את כל המזון
def print_food_db(food_df):
    print(reverse_text(" :מאגר המזון"))
    for _, data in food_df.iterrows():
        print_calculated_data(data)

