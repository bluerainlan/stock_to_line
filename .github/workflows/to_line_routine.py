import yfinance as yf
import requests
from datetime import datetime

LINE_NOTIFY_TOKEN = os.environ['LINE_NOTIFY_TOKEN']

def send_to_line(message):
    # 獲取當前時間
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 設置 Line Notify 的 API 地址和授權 token
    url = 'https://notify-api.line.me/api/notify'
    token=LINE_NOTIFY_TOKEN
    
    # 設置請求頭
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    
    # 將時間和訊息格式化成 Line Notify 的格式
    message_with_time = f"{message} \n {current_time}"
    
    # 設置要發送的消息內容
    send = {
        
        'message': message_with_time,
    }
    
    # 發送 POST 請求
    r = requests.post(url, headers=headers, data=send)
    print(r.text)

def get_real_time_stock_info(symbol, target_low_price, target_high_price):
    # 使用 yfinance 的 Ticker 物件來取得股票資訊
    ticker = yf.Ticker(symbol)
    
    # 獲取即時股票資訊
    real_time_info = ticker.info

    #獲取最低價和最高價
    low = real_time_info['regularMarketDayLow']
    high = real_time_info['regularMarketDayHigh']
    
    # 將目標價格轉換為浮點數
    target_low_price = float(target_low_price)
    target_high_price = float(target_high_price)
    
    # 準備股票資訊的格式化字串
    stock_info = f"股票代碼:{symbol}\n 股票類型:{real_time_info['quoteType']}"
    # 準備顯示的當前價格訊息
    current_price_info = f"目前最低價: {real_time_info['regularMarketDayLow']}\n 目前最高價: {real_time_info['regularMarketDayHigh']}"
    
    if low <= target_low_price:
        # 準備要發送的訊息
        message = f"{stock_info}\n {current_price_info}\n 最低價已達到設定值 {target_low_price}"
        send_to_line(message)
    elif high >= target_high_price:
        # 準備要發送的訊息
        message = f"{stock_info}\n {current_price_info}\n 最高價已達到設定值 {target_high_price}"
        send_to_line(message)

# 輸入要查詢的股票代碼
stock = '0050.TW' #如果要可以輸入股票代碼改=input('輸入要的股票代碼(台股後面需加.TW):')
stock_symbol = stock 
#輸入低價及高價
target_low_price = '154.5' # =input('輸入最低價:')
target_high_price = '156' # =input('輸入最高價:')

# 呼叫函式獲取即時股票資訊
get_real_time_stock_info(stock_symbol, target_low_price, target_high_price)
