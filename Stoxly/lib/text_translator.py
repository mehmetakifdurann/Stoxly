"""
Text Translator modülü - Finansal göstergeleri Türkçe mesajlara çevirir
"""
from typing import Optional
from lib.types import TechnicalIndicators, TranslatedInsights


def translate_indicators(indicators: TechnicalIndicators) -> TranslatedInsights:
    """
    Finansal göstergeleri Türkçe mesajlara çeviren ana fonksiyon
    """
    rsi_message = translate_rsi(indicators.rsi)
    risk_message = translate_risk(indicators.risk_score, indicators.volatility)
    trend_message = translate_trend(
        indicators.current_price,
        indicators.sma20,
        indicators.sma50,
        indicators.sma200
    )
    
    main_warning = determine_main_warning(indicators)
    main_action = determine_main_action(indicators)
    
    return TranslatedInsights(
        rsi_message=rsi_message,
        risk_message=risk_message,
        trend_message=trend_message,
        main_warning=main_warning,
        main_action=main_action
    )


def translate_rsi(rsi: float) -> str:
    """RSI değerini Türkçe mesaja çevir"""
    if rsi >= 80:
        return "Dikkat! Çok pahalı. Aşırı alım bölgesindesiniz."
    elif rsi >= 70:
        return "Pahalı. Alım için dikkatli olun."
    elif rsi >= 50:
        return "Nötr bölge. Fiyat dengeli görünüyor."
    elif rsi >= 30:
        return "Ucuz. Alım fırsatı olabilir."
    else:
        return "Çok ucuz! Aşırı satım bölgesindesiniz."


def translate_risk(risk_score: float, volatility: float) -> str:
    """Risk seviyesini Türkçe mesaja çevir"""
    if risk_score >= 70:
        return "Bu hisse Borsa'dan çok daha riskli. Yüksek volatilite var."
    elif risk_score >= 50:
        return "Bu hisse Borsa'dan daha riskli. Dikkatli olun."
    elif risk_score >= 30:
        return "Bu hisse Borsa ile benzer risk seviyesinde."
    else:
        return "Bu hisse Borsa'dan daha az riskli. Nispeten güvenli."


def translate_trend(
    current_price: float,
    sma20: float,
    sma50: float,
    sma200: float
) -> str:
    """Trend analizini Türkçe mesaja çevir"""
    above_20 = current_price > sma20
    above_50 = current_price > sma50
    above_200 = current_price > sma200
    
    if above_20 and above_50 and above_200:
        return "Güçlü yükseliş trendi. Tüm ortalamaların üzerinde."
    elif above_20 and above_50:
        return "Yükseliş trendi devam ediyor."
    elif above_20:
        return "Kısa vadede yükseliş var ama uzun vadede dikkatli olun."
    elif not above_20 and not above_50 and not above_200:
        return "Düşüş trendi. Tüm ortalamaların altında."
    else:
        return "Karışık sinyaller. Dikkatli olun."


def determine_main_warning(indicators: TechnicalIndicators) -> Optional[str]:
    """Ana uyarı mesajını belirle"""
    if indicators.rsi >= 80:
        return "Aşırı Alım Var!"
    elif indicators.rsi <= 20:
        return "Aşırı Satım Var!"
    elif indicators.risk_score >= 70:
        return "Yüksek Risk!"
    elif (
        indicators.current_price < indicators.sma200 and
        indicators.current_price < indicators.sma50
    ):
        return "Düşüş Trendi!"
    return None


def determine_main_action(indicators: TechnicalIndicators) -> Optional[str]:
    """Ana aksiyon mesajını belirle"""
    if indicators.rsi >= 80:
        return "Satış düşünebilirsiniz"
    elif indicators.rsi <= 20 and indicators.risk_score < 50:
        return "Alım fırsatı olabilir"
    elif (
        indicators.current_price > indicators.sma20 and
        indicators.current_price > indicators.sma50 and
        indicators.risk_score < 50
    ):
        return "Yükseliş trendi devam ediyor"
    return None


def get_risk_level(risk_score: float) -> str:
    """Risk seviyesi kategorisini belirle"""
    if risk_score < 30:
        return "Düşük"
    elif risk_score < 50:
        return "Orta"
    elif risk_score < 70:
        return "Yüksek"
    else:
        return "Çok Yüksek"

