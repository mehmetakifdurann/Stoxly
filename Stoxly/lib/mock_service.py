"""
Mock Data Service - Veri çekme servisi
Yahoo Finance API'sini kullanarak veya mock veri üretir
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional
from lib.types import PriceData, AssetType


def fetch_stock_data(ticker: str, period: str = "1y") -> List[PriceData]:
    """
    Yahoo Finance'dan hisse senedi verisi çek
    Borsa İstanbul için ticker formatı: GARAN.IS, AKBNK.IS vb.
    """
    try:
        # Borsa İstanbul için .IS ekle
        if not ticker.endswith('.IS') and not '.' in ticker:
            # Eğer crypto değilse Borsa İstanbul olarak dene
            ticker_with_suffix = f"{ticker}.IS"
        else:
            ticker_with_suffix = ticker
        
        stock = yf.Ticker(ticker_with_suffix)
        hist = stock.history(period=period)
        
        if hist.empty:
            # Eğer veri bulunamazsa mock veri döndür
            return generate_mock_data(ticker)
        
        price_data_list = []
        for date, row in hist.iterrows():
            price_data_list.append(PriceData(
                date=date.to_pydatetime(),
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                volume=float(row['Volume'])
            ))
        
        return price_data_list
    
    except Exception as e:
        print(f"Veri çekme hatası: {e}. Mock veri kullanılıyor.")
        return generate_mock_data(ticker)


def fetch_crypto_data(ticker: str, period: str = "1y") -> List[PriceData]:
    """
    Kripto para verisi çek
    """
    try:
        # Crypto için ticker formatı: BTC-USD, ETH-USD vb.
        if not '-' in ticker:
            ticker_with_suffix = f"{ticker}-USD"
        else:
            ticker_with_suffix = ticker
        
        crypto = yf.Ticker(ticker_with_suffix)
        hist = crypto.history(period=period)
        
        if hist.empty:
            return generate_mock_data(ticker, is_crypto=True)
        
        price_data_list = []
        for date, row in hist.iterrows():
            price_data_list.append(PriceData(
                date=date.to_pydatetime(),
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                volume=float(row['Volume'])
            ))
        
        return price_data_list
    
    except Exception as e:
        print(f"Veri çekme hatası: {e}. Mock veri kullanılıyor.")
        return generate_mock_data(ticker, is_crypto=True)


def generate_mock_data(ticker: str, is_crypto: bool = False) -> List[PriceData]:
    """
    Mock veri üret (test ve demo amaçlı)
    """
    import random
    import numpy as np
    
    # Başlangıç fiyatı
    if is_crypto:
        base_price = random.uniform(20000, 60000)  # Crypto için
    else:
        base_price = random.uniform(10, 200)  # Hisse için
    
    price_data_list = []
    current_price = base_price
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(252):  # 1 yıl için yaklaşık 252 iş günü
        date = start_date + timedelta(days=i)
        
        # Hafta sonlarını atla (basitleştirilmiş)
        if date.weekday() >= 5:
            continue
        
        # Random walk ile fiyat hareketi
        change_percent = random.uniform(-0.05, 0.05)
        current_price = current_price * (1 + change_percent)
        
        # OHLC verileri
        daily_volatility = random.uniform(0.01, 0.03)
        open_price = current_price
        high_price = open_price * (1 + random.uniform(0, daily_volatility))
        low_price = open_price * (1 - random.uniform(0, daily_volatility))
        close_price = open_price * (1 + random.uniform(-daily_volatility, daily_volatility))
        
        volume = random.uniform(1000000, 10000000)
        
        price_data_list.append(PriceData(
            date=date,
            open=round(open_price, 2),
            high=round(high_price, 2),
            low=round(low_price, 2),
            close=round(close_price, 2),
            volume=round(volume, 0)
        ))
    
    return price_data_list


def fetch_data(ticker: str, asset_type: AssetType, period: str = "1y") -> List[PriceData]:
    """
    Ana veri çekme fonksiyonu - asset type'a göre yönlendirir
    """
    if asset_type == "crypto":
        return fetch_crypto_data(ticker, period)
    else:
        return fetch_stock_data(ticker, period)

