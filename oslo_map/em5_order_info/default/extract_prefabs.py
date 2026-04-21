
import json
import glob

def find_prefab(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "Prefab":
                return value
            result = find_prefab(value)
            if result:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_prefab(item)
            if result:
                return result
    return None

def extract_prefabs():
    files = glob.glob("*.json")

    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            prefab = find_prefab(data)

            if prefab:
                print(f"{file}: {prefab}")
            else:
                print(f"{file}: No Prefab found")

        except Exception as e:
            print(f"{file}: Error - {e}")

extract_prefabs()
