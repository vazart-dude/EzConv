import requests
import csv
from bs4 import BeautifulSoup as BS 

def update_currency_rate():
    url = "https://www.cbr.ru/currency_base/daily/"
    class_ = "data"

    r = requests.get(url)
    html = BS(r.text, features="html.parser")
    t = html.find(class_=class_).text

    arr = t = t.split()[12:]
    t = "\n".join(t)

    with open("bin/currency_raw.txt", mode="w") as file:
        file.write(t)
        pass

    curr_values = []
    for num in arr:
        if "," in num:
            curr_values.append(num)

    # print(curr_values) #!

    with open("bin/currency.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";", quotechar='"')
        rows = [[value[0], value[1], value[2]] for value in reader]
        for x in range(len(curr_values)):
            rows[x][1] = curr_values[x].replace(',', '.')
        print(rows)
    with open("bin/currency.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(rows)
    with open("bin/log.txt", mode="w") as file: #TODO сделать логи
        pass
