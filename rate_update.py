import requests
import csv
import arrow
import os
import shutil

# Resource paths (read-only, bundled with app)
script_path = os.path.dirname(os.path.abspath(__file__))
resource_currency_path = os.path.join(script_path, "bin", "currency.csv")

# Writable data directory (user-specific)
app_data_dir = os.path.join(os.environ.get("APPDATA", script_path), "EzConv")
os.makedirs(app_data_dir, exist_ok=True)
log_path = os.path.join(app_data_dir, "log.txt")
currency_path = os.path.join(app_data_dir, "currency.csv")


def _ensure_data_files():
    """Copy currency data files from resources to writable app data dir if missing."""
    if not os.path.exists(currency_path):
        shutil.copy2(resource_currency_path, currency_path)


def update_currency_rate():
    _ensure_data_files()
    try:
        r = requests.get("https://open.er-api.com/v6/latest/RUB", timeout=10)
        r.raise_for_status()
        data = r.json()
        rates = data.get("rates", {})
        currency_map = {"GBR": "GBP"}

        with open(currency_path, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')
            rows = [[value[0], value[1], value[2]] for value in reader]

        for row in rows:
            code = row[0]
            api_code = currency_map.get(code, code)
            if api_code in rates and rates[api_code] != 0:
                row[1] = str((1 / rates[api_code]) * float(row[2]))

        with open(currency_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(rows)

        with open(log_path, mode="a") as file:
            file.write(f"currency updated {arrow.now().format('YYYY-MM-DD HH:mm')}\n")

        return True
    except Exception as e:
        print(e, "error")
        return False