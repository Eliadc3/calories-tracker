import parser
from display import print_calculated_data
from parser import calculate_row_data
from utils.text_utils import load_plural_map
# טוען את טבלת המזון וקובץ ההמרה מרבים ליחיד
food_df = parser.load_food_db()
plural_map = load_plural_map("data/food_singular_map.csv")

# קלט מהמשתמש
food_input = input("🔍 הכנס שם מזון: ")

# פונקציה שמקבלת שורה של מזון ומחזירה את הנתונים המחושבים
parser.parse_line(food_df, food_input, plural_map)

