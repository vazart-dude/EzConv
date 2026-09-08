import requests
import csv
import arrow
from dotenv import load_dotenv
import os


script_path = os.path.dirname(os.path.abspath(__file__))
crypto_currency_path = os.path.join(script_path, "bin", "crypto_currency.csv")
log_path = os.path.join(script_path, "bin", "log.txt")

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

load_dotenv()


def update_currency_rate_crypto():
    api_key = os.getenv("API_KEY")
    print("connected with api key:", api_key)  # key checking
    curr_values = []
    for coin in crypto_list:
        try:
            coin_api = coin[1]
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_api}&vs_currencies=rub&precision=4"
            headers = {
                "accept": "application/json",
                "x-cg-demo-api-key": api_key,
            }
            r = requests.get(url, headers=headers)
            data = r.json()
            coin_price = data[coin_api]["rub"]
            curr_values.append(float(coin_price))
        except Exception as e:
            print(f"Error: {e} for {coin[0]}")
            return False

    try:
        with open(crypto_currency_path, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')
            rows = [[value[0], value[1]] for value in reader]
            if len(curr_values) != len(rows):
                print(f"Length mismatch: got {len(curr_values)} values, expected {len(rows)}")
                return False
            for x in range(len(curr_values)):
                rows[x][1] = curr_values[x]
                rows[x].append(1)
            print("passed reader")
    except Exception as e:
        print("Error while reading currency:", e)
        return False

    try:
        with open(crypto_currency_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(rows)
            print("passed writer")
    except Exception as e:
        print("Error while writing currency:", e)
        return False

    with open(log_path, mode="a") as file:
        file.write(f"crypto updated {arrow.now().format('YYYY-MM-DD HH:mm')}\n")
    return True