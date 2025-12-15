from dataclasses import dataclass
from typing import List, Optional, Literal
from datetime import datetime

@dataclass
class PriceData:
    """Fiyat verisi için data class"""
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

@dataclass
class TechnicalIndicators:
    """Teknik göstergeler için data class"""
    rsi: float
    sma20: float
    sma50: float
    sma200: float
    risk_score: float
    volatility: float
    current_price: float

@dataclass
class TranslatedInsights:
    """Çevrilmiş içgörüler için data class"""
    rsi_message: str
    risk_message: str
    trend_message: str
    main_warning: Optional[str] = None
    main_action: Optional[str] = None

@dataclass
class AnalysisResult:
    """Analiz sonucu için data class"""
    indicators: TechnicalIndicators
    translated_insights: TranslatedInsights
    risk_level: Literal["Düşük", "Orta", "Yüksek", "Çok Yüksek"]

AssetType = Literal["stock", "crypto"]

