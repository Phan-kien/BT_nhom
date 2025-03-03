import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

# Danh sách các ví điện tử cần lấy dữ liệu (ID của CoinGecko)
cryptos = ['bitcoin', 'ethereum', 'binancecoin']

# Tạo một dictionary để lưu dữ liệu của các ví điện tử
crypto_data = {}

# Lấy dữ liệu cho mỗi ví điện tử
for crypto in cryptos:
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': '30'
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Chuyển dữ liệu thành DataFrame
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])

    # Chuyển đổi timestamp thành định dạng thời gian dễ đọc
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Sắp xếp lại dữ liệu theo ngày
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    # Tính toán các chỉ báo kỹ thuật
    df['MA10'] = df['price'].rolling(window=10).mean()  # Trung bình động 10 ngày
    df['MA20'] = df['price'].rolling(window=20).mean()  # Trung bình động 20 ngày

    # Tính toán chỉ số biến động
    df['daily_return'] = df['price'].pct_change()  # Tính lãi suất hàng ngày
    df['volatility'] = df['daily_return'].rolling(window=7).std() * np.sqrt(7)  # Biến động hàng tuần

    # Lưu DataFrame vào dictionary
    crypto_data[crypto] = df

# Vẽ biểu đồ cho tất cả các ví điện tử
plt.figure(figsize=(14, 10))

# Biểu đồ giá của các ví điện tử
plt.subplot(2, 1, 1)
for crypto in crypto_data:
    plt.plot(crypto_data[crypto].index, crypto_data[crypto]['price'], label=f'Giá {crypto.capitalize()} (USD)')
plt.title('Giá Các Ví Điện Tử trong 30 Ngày qua')
plt.xlabel('Ngày')
plt.ylabel('Giá (USD)')
plt.xticks(rotation=45)
plt.legend()
plt.grid()

# Biểu đồ biến động của các ví điện tử
plt.subplot(2, 1, 2)
for crypto in crypto_data:
    plt.plot(crypto_data[crypto].index, crypto_data[crypto]['volatility'], label=f'Biến động {crypto.capitalize()}')
plt.title('Biến Động Giá Các Ví Điện Tử (7 Ngày)')
plt.xlabel('Ngày')
plt.ylabel('Biến động (%)')
plt.xticks(rotation=45)
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

# Thông tin thống kê cho mỗi ví điện tử
for crypto in crypto_data:
    df = crypto_data[crypto]
    average_price = df['price'].mean()
    min_price = df['price'].min()
    max_price = df['price'].max()
    max_price_date = df[df['price'] == max_price].index[0]  # Ngày giá cao nhất
    min_price_date = df[df['price'] == min_price].index[0]  # Ngày giá thấp nhất

    print(f"\n{crypto.capitalize()} - Thống Kê:")
    print(f"Giá trung bình: ${average_price:.2f}")
    print(f"Giá thấp nhất: ${min_price:.2f} vào ngày {min_price_date.strftime('%Y-%m-%d')}")
    print(f"Giá cao nhất: ${max_price:.2f} vào ngày {max_price_date.strftime('%Y-%m-%d')}")

# Lưu dữ liệu vào CSV

