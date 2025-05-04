from binance.um_futures import UMFutures
import yfinance as yf
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator
import time
import hmac
import hashlib
import sys
from PyQt5.QtWidgets import *
from panel import *
from bot import *
import requests
import datetime
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from bs4 import BeautifulSoup
telegram_token = "*************************************************"#This place is hidden because api's can be used for personal usage
telegram_chat_id = "*************************************************"#This place is hidden because api's can be used for personal usage
BASE_URL = "https://fapi.binance.com"
API_SECRET = "*************************************************"#This place is hidden because api's can be used for personal usage
API_KEY = "*************************************************"#This place is hidden because api's can be used for personal usage
client = UMFutures(key=API_KEY, secret=API_SECRET)
headers = {"X-MBX-APIKEY": API_KEY}


def download_data(op, start_date, end_date):
    df = yf.download(op, start=start_date, end=end_date, progress=False)
    return df


stock = "BTC-USD"
today = datetime.date.today()
duration = 30
before = today - datetime.timedelta(days=duration)
start_date = before
end_date = today
data = download_data(stock, start_date, end_date)


def sign_request(params):
    params["timestamp"] = int(time.time() * 1000)
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    return params


def get_balance(symbol):
    params = sign_request({})
    url = f"{BASE_URL}/fapi/v2/balance"
    response = requests.get(url, params=params, headers=headers)
    balances = response.json()
    for balance in balances:
        if balance["asset"] == symbol:
            return balance["balance"]
    
def get_price(symbol):
    url = f"{BASE_URL}/fapi/v1/ticker/price"
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    return response.json()["price"]


uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_giris()
ui.setupUi(pencere)
pencere.show()
admin_login = False


def admin_giris():
    global admin_login
    admin_login = True
    check_login()


ui.pushButton_2.clicked.connect(lambda: admin_giris())

def check_login():
    username = ui.lineEdit.text()
    password = ui.lineEdit_2.text()

    if username == "ahmetyazici" and password == "123" or admin_login:
        main_window = Ui_main()
        main_window.setupUi(pencere)
        pencere.show()

        bakiye = get_balance("USDT")
        main_window.label_3.setText("PRICE:")
        main_window.label_5.setText("BALANCE:")
        main_window.label_6.setText(f"{bakiye} $")

        

        def fiyat_goster():
            
            fiyat = get_price(main_window.lineEdit.text())
            main_window.label_4.setText(f"{fiyat} $")

        main_window.pushButton.clicked.connect(fiyat_goster)

        stock = "BTC-USD"
        today = datetime.date.today()
        duration = 14
        before = today - datetime.timedelta(days=duration)
        start_date = before
        end_date = today

        def tech_indicators():
            option = main_window.comboBox.currentText().lower()
            close_series = data["Close"].squeeze()

            if option == "macd":
                macd = MACD(close_series).macd()
                macd_value = macd.iloc[-1]
                main_window.label_7.setText(f"MACD: {macd_value:.2f}")
            elif option == "rsi":
                rsi = RSIIndicator(close_series).rsi()
                rsi_value = rsi.iloc[-1]
                main_window.label_7.setText(f"RSI: {rsi_value:.2f}")
            elif option == "ema":
                ema = EMAIndicator(close_series, window=14).ema_indicator()
                ema_value = ema.iloc[-1]
                main_window.label_7.setText(f"EMA: {ema_value:.2f}")
            elif option == "sma":
                sma = SMAIndicator(close_series, window=14).sma_indicator()
                sma_value = sma.iloc[-1]
                main_window.label_7.setText(f"SMA: {sma_value:.2f}")
            else:
                main_window.label_7.setText("Select a valid option")

        def get_graphic():
            option = main_window.comboBox.currentText().lower()
            close_series = data["Close"].squeeze()

            if option == "macd":
                macd = MACD(close_series).macd()
                macd.plot(figsize=(12, 6), label="Indicator")
                plt.title('MACD')
                plt.xlabel('Date')
                plt.ylabel('Indicator')
                plt.legend()
                plt.grid(True)
                plt.show()

            elif option == "rsi":
                rsi = RSIIndicator(close_series).rsi()
                rsi.plot(figsize=(12, 6), label="Indicator")
                plt.title('RSI')
                plt.xlabel('Date')
                plt.ylabel('Indicator')
                plt.legend()
                plt.grid(True)
                plt.show()
            elif option == "ema":
                ema = EMAIndicator(close_series, window=14).ema_indicator()
                ema.plot(figsize=(12, 6), label="Indicator")
                plt.title('EMA')
                plt.xlabel('Date')
                plt.ylabel('Indicator')
                plt.legend()
                plt.grid(True)
                plt.show()
            elif option == "sma":
                sma = SMAIndicator(close_series, window=14).sma_indicator()
                sma.plot(figsize=(12, 6), label="Indicator")
                plt.title('SMA')
                plt.xlabel('Date')
                plt.ylabel('Indicator')
                plt.legend()
                plt.grid(True)
                plt.show()

        last_action = None

        def get_live_data():
            end = datetime.datetime.now()
            start = end - datetime.timedelta(days=5)
            df = yf.download("BTC-USD", start=start, end=end, interval="1h", progress=False)
            return df
        isActive=False

        def start_bot():
            price = float(get_price(main_window.lineEdit.text()))
            option = main_window.comboBox.currentText().lower()
            close_series = data["Close"].squeeze()
            macd = MACD(close_series).macd()
            macd_value = MACD(close_series).macd().iloc[-1]
            rsi = RSIIndicator(close_series).rsi()
            rsi_value = RSIIndicator(close_series).rsi().iloc[-1]
            sma = SMAIndicator(close_series, window=14).sma_indicator()            
            ema_value = EMAIndicator(close_series, window=14).ema_indicator().iloc[-1]

            if macd_value > 0 or 40 < rsi_value < 80 or (price - ema_value) > 0 :
                action = "BUY"
                temp=price
            elif macd_value > 0 or rsi_value > 90 or (price - ema_value) > 0 or price>temp:
                action = "SELL"
            else:
                action = "HOLD"
                
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row_position = main_window.tableWidget.rowCount()
            main_window.tableWidget.insertRow(row_position)
            main_window.tableWidget.setItem(row_position, 0, QTableWidgetItem(current_time))
            main_window.tableWidget.setItem(row_position, 1, QTableWidgetItem(action))
            main_window.tableWidget.setItem(row_position, 2, QTableWidgetItem(f"{price} $"))
            token = "7064774305:AAEPDZoSSOOhtt_pKsDTSL-hea-1D2oHBws"
            chat_id = "-1002016473516"
            message = f"📈 İşlem Zamanı: {current_time}\nAksiyon: {action}\nFiyat: {price} $"
            api_url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(api_url, data={"chat_id": chat_id, "text": message})
        
        
        
        main_window.pushButton_5.clicked.connect(get_graphic)
        main_window.pushButton_4.clicked.connect(tech_indicators)
        def start_bot_timer():
            main_window.isActive.setText("Bot Çalışıyor...")
            main_window.timer_bot = QTimer()
            main_window.timer_bot.timeout.connect(fiyat_goster)
            main_window.timer_bot.timeout.connect(start_bot)
            main_window.timer_bot.start(5000)
        main_window.pushButton_2.clicked.connect(start_bot_timer)
        def stop_bot_timer():
            main_window.isActive.setText("Bot Çalışmayı Durdurdu...")
            if hasattr(main_window, 'timer_bot') and main_window.timer_bot.isActive():
                main_window.timer_bot.stop()
        main_window.pushButton_3.clicked.connect(stop_bot_timer)

    else:
        QMessageBox.warning(pencere, "Hatalı Giriş", "Kullanıcı adı veya şifre yanlış!")

ui.pushButton.clicked.connect(check_login)

sys.exit(uygulama.exec_())
