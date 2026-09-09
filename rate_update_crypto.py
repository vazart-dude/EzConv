import requests
import csv
import arrow
import os

script_path = os.path.dirname(os.path.abspath(__file__))
crypto_currency_path = os.path.join(script_path, "bin", "crypto_currency.csv")
log_path = os.path.join(script_path, "bin", "log.txt")

crypto_list = (
    ["BTC", "bitcoin"],
    ["ETH", "ethereum"],
    ["USDT", "tether"],
    ["SOL", "solana"],
    ["BNB", "binance-coin"],
    ["DOGE", "dogecoin"],
    ["TRX", "tron"],
    ["XRP", "ripple"],
    ["TON", "the-open-network"],
)


def update_currency_rate_crypto():
    try:
        usd_rub_r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
        usd_rub_r.raise_for_status()
        usd_rub = usd_rub_r.json().get("rates", {}).get("RUB")
        if usd_rub is None:
            print("USD/RUB rate not found")
            return False

        ids = ",".join(coin[1] for coin in crypto_list)
        url = f"https://api.coincap.io/v2/assets?ids={ids}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json().get("data", [])

        prices = {}
        for asset in data:
            prices[asset["id"]] = float(asset["priceUsd"])

        curr_values = []
        for coin in crypto_list:
            coin_id = coin[1]
            if coin_id in prices:
                curr_values.append(prices[coin_id] * usd_rub)
            else:
                print(f"Price not found for {coin_id}")
                return False

        with open(crypto_currency_path, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')
            rows = [[value[0], value[1]] for value in reader]
            if len(curr_values) != len(rows):
                print(
                    f"Length mismatch: got {len(curr_values)} values, expected {len(rows)}"
                )
                return False
            for x in range(len(curr_values)):
                rows[x][1] = curr_values[x]  # ty: ignore[invalid-assignment]
                rows[x].append(1)  # ty: ignore[invalid-argument-type]
    except Exception as e:
        print("Error while reading currency:", e)
        return False

    try:
        with open(crypto_currency_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(rows)
    except Exception as e:
        print("Error while writing currency:", e)
        return False

    with open(log_path, mode="a") as file:
        file.write(f"crypto updated {arrow.now().format('YYYY-MM-DD HH:mm')}\n")
    return True
