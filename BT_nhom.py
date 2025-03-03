import requests
import time
import matplotlib.pyplot as plt

def get_crypto_prices():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "67353284-595e-490e-a5a7-7e87cbbde307"
    }
    params = {"start": "1", "limit": "10", "convert": "USD"}  # Lấy 10 coin đầu tiên

    previous_prices = {}  # Để lưu giá trước đó

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if "data" in data:
            crypto_data = {}
            for coin in data["data"]:
                name = coin["name"]
                price = coin["quote"]["USD"]["price"]
                crypto_data[name] = price

            # Vẽ biểu đồ mới
            plt.figure(figsize=(8, 5))

            # Xác định màu sắc cho mỗi cột dựa trên giá trước đó
            colors = []
            for name in crypto_data.keys():
                if name in previous_prices:
                    if crypto_data[name] > previous_prices[name]:  # Giá tăng
                        colors.append('green')
                    elif crypto_data[name] < previous_prices[name]:  # Giá giảm
                        colors.append('red')
                    else:  # Giá không thay đổi
                        colors.append('blue')
                else:
                    colors.append('blue')  # Nếu không có giá trước đó, chọn màu khác

            plt.bar(crypto_data.keys(), crypto_data.values(), color=colors)
            plt.title("ccCrypto Prices")
            plt.xlabel("Cryptocurrency")
            plt.ylabel("Price (USD)")
            plt.ylim(0, max(crypto_data.values()) * 1.2)  # Để biểu đồ không bị dính sát mép

            for i, (name, price) in enumerate(crypto_data.items()):
                plt.text(i, price, f"${price:.2f}", ha='center', va='bottom', fontsize=12)

            plt.show()
            plt.pause(1)
            plt.close()

            # Cập nhật giá trước đó
            previous_prices = crypto_data

        else:
            print("Lỗi lấy dữ liệu:", data)

        time.sleep(10)  # Cập nhật mỗi 10 giây

if __name__ == "__main__":
    get_crypto_prices()


