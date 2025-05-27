import csv

def load_translation_map(path):
    translations = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            translations[row['english'].strip()] = row['hebrew'].strip()
    return translations

def translate_items(items, translation_map):
    return [translation_map.get(item, item) for item in items]