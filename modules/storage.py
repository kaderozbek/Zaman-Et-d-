# path: modules/storage.py

import json
import os

def load_data(path="veri_kaydi.json"):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # bozuk dosyayı kurtarmak için boş sözlük döndür
        return {}

def save_data(data, file_path="veri_kaydi.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
