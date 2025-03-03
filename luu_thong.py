import requests

API_KEY = "67353284-595e-490e-a5a7-7e87cbbde307"
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY
}
params = {"start": "1", "limit": "5", "convert": "USD"}  # Lấy 5 coin hàng đầu

response = requests.get(url, headers=headers, params=params)
data = response.json()

if "data" in data:
    for coin in data["data"]:
        name = coin["name"]
        symbol = coin["symbol"]
        price = coin["quote"]["USD"]["price"]
        volume_24h = coin["quote"]["USD"]["volume_24h"]
        market_cap = coin["quote"]["USD"]["market_cap"]
        circulating_supply = coin["circulating_supply"]

        print(f"{name} ({symbol})")
        print(f"   💰 Giá: ${price:.2f}")
        print(f"   📊 Khối lượng giao dịch 24h: ${volume_24h:,.2f}")
        print(f"   🌍 Vốn hóa thị trường: ${market_cap:,.2f}")
        print(f"   🔄 Cung lưu hành: {circulating_supply:,.2f} {symbol}\n")

else:
    print("Không lấy được dữ liệu:", data)
