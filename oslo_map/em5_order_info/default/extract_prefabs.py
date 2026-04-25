import json
import glob
import os
from datetime import datetime
from collections import defaultdict

def find_prefab(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "Prefab":
                return value
            result = find_prefab(value)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_prefab(item)
            if result is not None:
                return result
    return None

def get_category(filename):
    name = os.path.splitext(filename)[0].lower()

    # Any filename containing "pol" goes to POLICE
    if "pol" in name:
        return "POLICE"

    # RTW anywhere in filename (rtw1, my_rtw_backup, etc.)
    if "rtw" in name:
        return "RTW"

    # Combined categories
    if "irtw" in name or "iktw" in name:
        return "IKTW / IRTW"

    if "ktw" in name:
        return "KTW"

    if "naw" in name:
        return "NAW"

    if "manv" in name:
        return "MANV"

    if "legevakt" in name:
        return "NEF"

    # Standard categories
    categories = [
        "nef", "lna", "hlf", "lf", "rw", "dlk",
        "gwl", "wlf", "mtw", "tlf", "kef",
        "elw", "kdow", "osf", "asf"
    ]

    for cat in categories:
        if cat in name:
            return cat.upper()

    return "OTHER"

def extract_prefabs():
    files = glob.glob("*.json")
    grouped = defaultdict(list)

    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            prefab = find_prefab(data)

            if prefab is not None:
                line = f"{file}: {prefab}"
            else:
                line = f"{file}: No Prefab found"

        except Exception as e:
            line = f"{file}: Error - {e}"

        category = get_category(file)
        grouped[category].append(line)

    output_file = datetime.now().strftime("%Y-%m-%d.txt")

    with open(output_file, "w", encoding="utf-8") as out:
        for category in sorted(grouped.keys()):
            header = f"===== {category} ====="
            print(header)
            out.write(header + "\n")

            for line in sorted(grouped[category]):
                print(line)
                out.write(line + "\n")

            out.write("\n")

    print(f"\nResults saved to {output_file}")

extract_prefabs()