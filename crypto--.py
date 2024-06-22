import requests 
from urllib.request import urlopen
from bs4 import BeautifulSoup 
import numpy as np 
from urllib.error import URLError 
from time import sleep 
 
# آدرس‌های URL برای CoinRanking و CoinMarketCap 
coinranking_url = "https://api.coinranking.com/v2/coins" 
coinmarketcap_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest" 
coinmarketcap_api_key = "YOUR_COINMARKETCAP_API_KEY" 
 
# هدرهای لازم برای استفاده از API CoinMarketCap 
coinmarketcap_headers = { 
    'Accepts': 'application/json', 
    'X-CMC_PRO_API_KEY': coinmarketcap_api_key, 
} 
 
# تابع برای دریافت داده‌ها از CoinRanking 
def get_coinranking_data(): 
    response = requests.get(coinranking_url) 
    data = response.json() 
    coins = data['data']['coins'] 
    coinranking_prices = {coin['symbol']: float(coin['price']) for coin in coins[:10]} 
    return coinranking_prices 
 
# تابع برای دریافت داده‌ها از CoinMarketCap 
def get_coinmarketcap_data(): 
    response = requests.get(coinmarketcap_url, headers=coinmarketcap_headers) 
    data = response.json() 
    coins = data['data'] 
    coinmarketcap_prices = {coin['symbol']: coin['quote']['USD']['price'] for coin in coins[:10]} 
    return coinmarketcap_prices 
 
# تابع برای استخراج قیمت‌ها از جدول HTML 
def extract_prices_from_html(url): 
    try: 
        html = urlopen(url) 
        bs = BeautifulSoup(html.read(), 'lxml') 
 
        # استخراج تمام ردیف‌های جدول 
        table_rows = bs.find_all('div', {'class': 'valuta'}) 
 
        prices = [] 
 
        # استخراج و تبدیل قیمت‌ها به عدد شناور 
        for i in range(len(table_rows)): 
            price_string = table_rows[i].get_text().replace('$', '').replace(' ', '').replace('\n', '').replace(',', '') 
            try: 
                price = float(price_string) 
                prices.append(price) 
            except ValueError: 
                continue  # اگر تبدیل به عدد امکان‌پذیر نبود، ادامه دهید 
 
        return prices 
 
    except URLError as e: 
        print("باید به اینترنت متصل شوید") 
        sleep(1) 
        return [] 
 
# دریافت داده‌ها از هر دو API 
coinranking_prices = get_coinranking_data() 
coinmarketcap_prices = get_coinmarketcap_data() 
 
# مقایسه قیمت‌ها و پیدا کردن ارزهای ارزان‌تر 
cheaper_coins = {} 
for symbol in coinranking_prices: 
    if symbol in coinmarketcap_prices: 
        coinranking_price = coinranking_prices[symbol] 
        coinmarketcap_price = coinmarketcap_prices[symbol] 
        cheaper_price = min(coinranking_price, coinmarketcap_price) 
        cheaper_coins[symbol] = cheaper_price 
 
# نمایش ارزهای ارزان‌تر 
print("مقایسه ارزهای ارزان‌تر:") 
for symbol, price in cheaper_coins.items(): 
    print(f"{symbol}: ${price:.2f}") 
 
print("*-----------------------------------------------------------------*") 
 
# مثال استفاده از تابع استخراج قیمت‌ها از HTML 
urlinput = input("لطفا یک لینک وارد کنید (بدون https://): ") 
full_url = "https://" + urlinput 
prices = extract_prices_from_html(full_url) 
 
# تقسیم قیمت‌ها به دسته‌های پنج تایی و محاسبه میانگین هر دسته 
for i in range(0, len(prices), 5): 
    batch = prices[i:i + 5] 
    if batch: 
        average_price = np.mean(batch) 
        print(f"دسته {i // 5 + 1}: {batch}") 
        print(f"میانگین قیمت: {average_price:.2f}") 
        print("******************************************")