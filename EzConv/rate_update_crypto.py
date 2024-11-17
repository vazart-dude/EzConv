import requests
import csv
import arrow
from bs4 import BeautifulSoup as BS

crypto_list = (
    ["BTC", "bitcoin"],
    ["ETH", "ethereum"],
    ["USDT", "tether"],
    ["SOL", "solana"],
    ["BNB", "binancecoin"],
    ["DOGE", "dogecoin"],
    ["TRX", "tron"],
    ["XRP", "ripple"],
    ["TON", "the-open-network"],
)

curr_values = []

#!! Т.к. API бесплатный то он имеет ограничения по кол-ву запросов в месяц и минуту
#!! использовать осторожно

def update_currency_rate_crypto():
    for coin in crypto_list:
        try:
            # x = '1' + 0 #! для активации ошибки, чтобы не тратился API
            coin_api = coin[1]
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_api}&vs_currencies=rub&precision=4"
            headers = {"accept": "application/json", "x-cg-demo-api-key": "CG-Nq3bK18xPt48dFjK4u5yR5uy"}
            r = requests.get(url, headers=headers)   
            data = r.json()
            coin_price = data[coin_api]['rub']
            curr_values.append(float(coin_price))
        except Exception as e:
            print(f"Error: {e} for {coin[0]}")
            return True
        
    with open("bin/crypto_currency.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";", quotechar='"')
        rows = [[value[0], value[1]] for value in reader]
        for x in range(len(curr_values)):
            rows[x][1] = curr_values[x]
            rows[x].append(1)
        print("passed reader")
    
    with open("bin/crypto_currency.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(rows)
        print("passed writer")
    
    with open("bin/log.txt", mode="a") as file: #TODO// сделать логи
        file.write(f'ccrypto updated {arrow.now().format('YYYY-MM-DD HH:mm')}\n')




#update_currency_rate_crypto()

