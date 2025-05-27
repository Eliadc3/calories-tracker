import csv
import re

# הפוך טקסט
def reverse_text(text):
    return text[::-1]

# טוען טבלת רבים → יחיד
def load_plural_map(file_path):
    plural_map = {}
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            plural_map[row["רבים"].strip()] = row["יחיד"].strip()
    return plural_map

# טוען טבלת יחידות → גרמים
def load_unit_weights(file_path):
    unit_weights = {}
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            unit_weights[row["יחידה"].strip()] = float(row["גרמים"])
    return unit_weights

# מחלץ את כל היחידות (יחיד + רבים) מתוך קובץ המרה
def get_all_units(file_path):
    units = set()
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            units.add(row["יחיד"].strip())
            units.add(row["רבים"].strip())
    return list(units)

# מנתח קלט של מזון כמו "2 כוסות המבורגר"
def parse_input_line(food_input):
    food_input = food_input.strip()

    # טוען את רשימת היחידות באופן דינמי
    unit_list = get_all_units("data/unit_singular_map.csv")
    units_pattern = "|".join(sorted(unit_list, key=len, reverse=True))  # הכי ארוך קודם

    patterns = [
        rf"^(\d+(?:\.\d+)?)\s*({units_pattern})\s+(.+)$",     # כמות → יחידה → שם
        rf"^(.+?)\s+(\d+(?:\.\d+)?)\s*({units_pattern})$",    # שם → כמות → יחידה
    ]

    for i, pattern in enumerate(patterns):
        match = re.match(pattern, food_input)
        if match:
            if i == 1:
                name = match.group(1)
                quantity = float(match.group(2))
                unit = match.group(3)
            else:
                quantity = float(match.group(1))
                unit = match.group(2)
                name = match.group(3)
            return {"name": name.strip(), "quantity": quantity, "unit": unit.strip()}

    # תבנית בסיסית: מספר + שם
    basic_match = re.match(r"^(\d+(?:\.\d+)?)\s+(.+)$", food_input)
    if basic_match:
        return {
            "name": basic_match.group(2).strip(),
            "quantity": float(basic_match.group(1)),
            "unit": None
        }

    # אם מתחיל ביחידת מידה בלי מספר
    for unit in unit_list:
        if food_input.startswith(unit + " "):
            name = food_input[len(unit):].strip()
            return {
                "name": name,
                "quantity": 1,
                "unit": unit
            }

    # ברירת מחדל: הכל שם המזון
    return {
        "name": food_input,
        "quantity": 1,
        "unit": None
    }
