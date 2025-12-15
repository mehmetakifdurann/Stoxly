"""
Finansal analiz modülü - Teknik göstergelerin hesaplanması
"""
import numpy as np
import pandas as pd
from typing import List
from lib.types import PriceData, TechnicalIndicators


def calculate_rsi(prices: List[PriceData], period: int = 14) -> float:
    """
    RSI (Relative Strength Index) hesaplama
    RSI 0-100 arasında bir değerdir
    """
    if len(prices) < period + 1:
        return 50.0  # Yeterli veri yoksa nötr değer
    
    closes = [p.close for p in prices]
    gains = []
    losses = []
    
    for i in range(1, len(closes)):
        change = closes[i] - closes[i - 1]
        gains.append(change if change > 0 else 0)
        losses.append(abs(change) if change < 0 else 0)
    
    # Son period kadar veriyi al
    recent_gains = gains[-period:]
    recent_losses = losses[-period:]
    
    avg_gain = sum(recent_gains) / period
    avg_loss = sum(recent_losses) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return round(rsi, 2)


def calculate_sma(prices: List[PriceData], period: int) -> float:
    """
    Simple Moving Average (SMA) hesaplama
    """
    if len(prices) < period:
        return prices[-1].close if prices else 0.0
    
    recent_prices = prices[-period:]
    sma = sum(p.close for p in recent_prices) / period
    
    return round(sma, 2)


def calculate_volatility(prices: List[PriceData], period: int = 20) -> float:
    """
    Volatilite (Risk) hesaplama
    Standart sapma kullanarak volatiliteyi hesaplar
    """
    if len(prices) < period:
        return 0.0
    
    recent_prices = prices[-period:]
    closes = [p.close for p in recent_prices]
    
    mean = sum(closes) / len(closes)
    variance = sum((price - mean) ** 2 for price in closes) / len(closes)
    std_dev = np.sqrt(variance)
    volatility = (std_dev / mean) * 100  # Yüzde olarak
    
    return round(volatility, 2)


def calculate_risk_score(prices: List[PriceData], volatility: float) -> float:
    """
    Risk Skoru hesaplama (0-100 arası)
    Volatilite ve fiyat hareketlerine göre
    """
    # Volatilite bazlı risk (0-70 puan)
    volatility_risk = min(volatility * 2, 70)
    
    # Son 20 günlük fiyat değişimine göre risk (0-30 puan)
    if len(prices) < 20:
        return round(volatility_risk)
    
    recent_20 = prices[-20:]
    price_change = ((recent_20[-1].close - recent_20[0].close) / recent_20[0].close) * 100
    
    volatility_risk_2 = abs(price_change) * 0.5
    additional_risk = min(volatility_risk_2, 30)
    
    total_risk = volatility_risk + additional_risk
    return min(round(total_risk), 100)


def calculate_all_indicators(prices: List[PriceData]) -> TechnicalIndicators:
    """
    Tüm teknik göstergeleri hesapla
    """
    rsi = calculate_rsi(prices)
    sma20 = calculate_sma(prices, 20)
    sma50 = calculate_sma(prices, 50)
    sma200 = calculate_sma(prices, 200)
    volatility = calculate_volatility(prices)
    risk_score = calculate_risk_score(prices, volatility)
    current_price = prices[-1].close if prices else 0.0
    
    return TechnicalIndicators(
        rsi=rsi,
        sma20=sma20,
        sma50=sma50,
        sma200=sma200,
        risk_score=risk_score,
        volatility=volatility,
        current_price=current_price
    )

