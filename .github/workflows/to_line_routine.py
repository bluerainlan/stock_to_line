import os
import yfinance as yf
import requests
from datetime import datetime
import json


# 設定環境變數
os.environ['LINE_BOT_ACCESS_TOKEN'] = "pFPZ6uGlF7Vk49qUP/JiNxCdNoO4isBdzEuBYQIaNSyMWRudFryMkiXSsGE629grbE2hXKYq6kL1++X3YotEY71O+DAML3Dh5YcaaxKYZ4FuvvAjiNwZGEt2IrzhSm8DKvEt9Gduei+GLr1K5EqVbgdB04t89/1O/w1cDnyilFU="
os.environ['LINE_USER_ID'] = "U3d20862812157dc4e0dd7736bebb31d7"

# 讀取環境變數
LINE_BOT_ACCESS_TOKEN = os.getenv("LINE_BOT_ACCESS_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

def send_to_line(message):
    # 取得當前時間
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 設定 API URL
    url = "https://api.line.me/v2/bot/message/push"

    # 設定請求標頭
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_BOT_ACCESS_TOKEN}",
    }

    # 訊息內容
    message_with_time = f"{message} \n {current_time}"
    data = {
        "to": USER_ID,
        "messages": [
            {"type": "text", "text": message_with_time}
        ]
    }

    # 發送 POST 請求
    response = requests.post(url, headers=headers, data=json.dumps(data))



def get_real_time_stock_info(symbol, target_low_price, target_high_price):
    # 使用 yfinance 的 Ticker 物件來取得股票資訊
    ticker = yf.Ticker(symbol)
    
    # 獲取即時股票資訊
    real_time_info = ticker.info

    #獲取一天的最新股價
    stock_price = ticker.history(period='1d')

    #獲取最低價和最高價
    low = real_time_info['regularMarketDayLow']
    high = real_time_info['regularMarketDayHigh']
    #獲取一天歷史價格接近的收盤價
    now = stock_price['Close'].iloc[-1]
    
    # 將目標價格轉換為浮點數
    target_low_price = float(target_low_price)
    target_high_price = float(target_high_price)
    now_price =  f"{now:.2f}"

    
    # 準備股票資訊的格式化字串
    stock_info = f" 股票代碼:{symbol}\n 股票名稱:{real_time_info['longName']}\n 股票類型:{real_time_info['quoteType']}"
    # 準備顯示的當前價格訊息
    current_price_info = f"目前價格: {now_price}\n 目前最低價: {real_time_info['regularMarketDayLow']}\n 目前最高價: {real_time_info['regularMarketDayHigh']}"
    
    if low <= target_low_price:
        # 準備要發送的訊息
        message = f"{stock_info}\n {current_price_info}\n 已達到最低價設定值 {target_low_price}"
        send_to_line(message)
    elif high >= target_high_price:
        # 準備要發送的訊息
        message = f"{stock_info}\n {current_price_info}\n 已達到最高價設定值 {target_high_price}"
        send_to_line(message)

# 輸入要查詢的股票代碼
stock = '2330.TW' #如果要可以輸入股票代碼改=input('輸入要的股票代碼(台股後面需加.TW):')
stock_symbol = stock 
#輸入低價及高價
target_low_price = '1000' # =input('輸入最低價:')
target_high_price = '1500' # =input('輸入最高價:')

# 呼叫函式獲取即時股票資訊
get_real_time_stock_info(stock_symbol, target_low_price, target_high_price)
