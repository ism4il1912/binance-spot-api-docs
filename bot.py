import ccxt
import time
import pandas as pd
import numpy as np

# Binance API anahtarlarınızı buraya girin
API_KEY = 'xpy2IY2OuNkVtPGdMDL7mLEc1hCyb0UOle9Nt9lPRzN6x8AisQQHHxg4KKy26ZMw'
SECRET_KEY = 'Ed25519, RSA'

# Binance bağlantısı
exchange = ccxt.binance({
    'apiKey': xpy2IY2OuNkVtPGdMDL7mLEc1hCyb0UOle9Nt9lPRzN6x8AisQQHHxg4KKy26ZMw

,
    'secret': Ed25519, RSA,
})

# Ticaret yapılacak sembol ve zaman aralığı
symbol = 'BTC/USDT'
timeframe = '1h'  # 1 saatlik mum verileri

# Strateji parametreleri
short_ma_period = 10  # Kısa vadeli hareketli ortalama
long_ma_period = 50   # Uzun vadeli hareketli ortalama
rsi_period = 14       # RSI periyodu
rsi_overbought = 70   # Aşırı alım seviyesi
rsi_oversold = 30     # Aşırı satım seviyesi

# Hareketli ortalama hesaplama fonksiyonu
def calculate_moving_average(data, period):
    return data['close'].rolling(window=period).mean()

# RSI hesaplama fonksiyonu
def calculate_rsi(data, period):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Sonsuz döngüde botu çalıştır
while True:
    try:
        # Son mum verilerini al
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # Hareketli ortalamaları hesapla
        df['short_ma'] = calculate_moving_average(df, short_ma_period)
        df['long_ma'] = calculate_moving_average(df, long_ma_period)

        # RSI hesapla
        df['rsi'] = calculate_rsi(df, rsi_period)

        # Son değerleri al
        last_row = df.iloc[-1]
        short_ma = last_row['short_ma']
        long_ma = last_row['long_ma']
        rsi = last_row['rsi']

        # Alım-satım stratejisi
        if short_ma > long_ma and rsi < rsi_oversold:
            print("Alım Sinyali! Kısa MA, Uzun MA'nın üzerinde ve RSI aşırı satımda.")
            # Örnek alım emri (0.001 BTC al)
            # order = exchange.create_market_buy_order(symbol, 0.001)
            # print("Alım Emri:", order)
        elif short_ma < long_ma and rsi > rsi_overbought:
            print("Satım Sinyali! Kısa MA, Uzun MA'nın altında ve RSI aşırı alımda.")
            # Örnek satım emri (0.001 BTC sat)
            # order = exchange.create_market_sell_order(symbol, 0.001)
            # print("Satım Emri:", order)

        # 1 saat bekle (zaman aralığına göre ayarlayın)
        time.sleep(60 * 60)

    except Exception as e:
        print("Hata:", e)
        time.sleep(60)  # Hata durumunda 1 dakika bekle
