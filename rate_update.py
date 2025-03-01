import requests
import csv
import arrow
from bs4 import BeautifulSoup as BS
import os

script_path = os.path.dirname(os.path.abspath(__file__))
currency_path = os.path.join(script_path, "bin", "currency.csv")
log_path = os.path.join(script_path, "bin", "log.txt")


def update_currency_rate():
    try:
        url = "https://www.cbr.ru/currency_base/daily/"
        class_ = "data"

        r = requests.get(url)
        html = BS(r.text, features="html.parser")
        t = html.find(class_=class_).text

        arr = t = t.split()[12:]

        curr_values = []
        for num in arr:
            if "," in num:
                curr_values.append(num)

        # print(curr_values) #!

        with open(currency_path, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')
            rows = [[value[0], value[1], value[2]] for value in reader]
            for x in range(len(curr_values)):
                rows[x][1] = curr_values[x].replace(",", ".")
            # print(rows)
        with open(currency_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(rows)

        with open(log_path, mode="a") as file:  # TODO// сделать логи
            file.write(f"currency updated {arrow.now().format('YYYY-MM-DD HH:mm')}\n")
    except Exception as e:
        print(e, "error")
