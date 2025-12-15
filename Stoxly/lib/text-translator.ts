import { TechnicalIndicators, TranslatedInsights } from "./types";

/**
 * Finansal göstergeleri Türkçe mesajlara çeviren ana fonksiyon
 */
export function translateIndicators(
  indicators: TechnicalIndicators
): TranslatedInsights {
  const rsiMessage = translateRSI(indicators.rsi);
  const riskMessage = translateRisk(indicators.riskScore, indicators.volatility);
  const trendMessage = translateTrend(
    indicators.currentPrice,
    indicators.sma20,
    indicators.sma50,
    indicators.sma200
  );

  const mainWarning = determineMainWarning(indicators);
  const mainAction = determineMainAction(indicators);

  return {
    rsiMessage,
    riskMessage,
    trendMessage,
    mainWarning,
    mainAction,
  };
}

/**
 * RSI değerini Türkçe mesaja çevir
 */
function translateRSI(rsi: number): string {
  if (rsi >= 80) {
    return "Dikkat! Çok pahalı. Aşırı alım bölgesindesiniz.";
  } else if (rsi >= 70) {
    return "Pahalı. Alım için dikkatli olun.";
  } else if (rsi >= 50) {
    return "Nötr bölge. Fiyat dengeli görünüyor.";
  } else if (rsi >= 30) {
    return "Ucuz. Alım fırsatı olabilir.";
  } else {
    return "Çok ucuz! Aşırı satım bölgesindesiniz.";
  }
}

/**
 * Risk seviyesini Türkçe mesaja çevir
 */
function translateRisk(riskScore: number, volatility: number): string {
  if (riskScore >= 70) {
    return "Bu hisse Borsa'dan çok daha riskli. Yüksek volatilite var.";
  } else if (riskScore >= 50) {
    return "Bu hisse Borsa'dan daha riskli. Dikkatli olun.";
  } else if (riskScore >= 30) {
    return "Bu hisse Borsa ile benzer risk seviyesinde.";
  } else {
    return "Bu hisse Borsa'dan daha az riskli. Nispeten güvenli.";
  }
}

/**
 * Trend analizini Türkçe mesaja çevir
 */
function translateTrend(
  currentPrice: number,
  sma20: number,
  sma50: number,
  sma200: number
): string {
  const above20 = currentPrice > sma20;
  const above50 = currentPrice > sma50;
  const above200 = currentPrice > sma200;

  if (above20 && above50 && above200) {
    return "Güçlü yükseliş trendi. Tüm ortalamaların üzerinde.";
  } else if (above20 && above50) {
    return "Yükseliş trendi devam ediyor.";
  } else if (above20) {
    return "Kısa vadede yükseliş var ama uzun vadede dikkatli olun.";
  } else if (!above20 && !above50 && !above200) {
    return "Düşüş trendi. Tüm ortalamaların altında.";
  } else {
    return "Karışık sinyaller. Dikkatli olun.";
  }
}

/**
 * Ana uyarı mesajını belirle
 */
function determineMainWarning(indicators: TechnicalIndicators): string | undefined {
  if (indicators.rsi >= 80) {
    return "Aşırı Alım Var!";
  } else if (indicators.rsi <= 20) {
    return "Aşırı Satım Var!";
  } else if (indicators.riskScore >= 70) {
    return "Yüksek Risk!";
  } else if (
    indicators.currentPrice < indicators.sma200 &&
    indicators.currentPrice < indicators.sma50
  ) {
    return "Düşüş Trendi!";
  }
  return undefined;
}

/**
 * Ana aksiyon mesajını belirle
 */
function determineMainAction(indicators: TechnicalIndicators): string | undefined {
  if (indicators.rsi >= 80) {
    return "Satış düşünebilirsiniz";
  } else if (indicators.rsi <= 20 && indicators.riskScore < 50) {
    return "Alım fırsatı olabilir";
  } else if (
    indicators.currentPrice > indicators.sma20 &&
    indicators.currentPrice > indicators.sma50 &&
    indicators.riskScore < 50
  ) {
    return "Yükseliş trendi devam ediyor";
  }
  return undefined;
}

/**
 * Risk seviyesi kategorisini belirle
 */
export function getRiskLevel(riskScore: number): "Düşük" | "Orta" | "Yüksek" | "Çok Yüksek" {
  if (riskScore < 30) return "Düşük";
  if (riskScore < 50) return "Orta";
  if (riskScore < 70) return "Yüksek";
  return "Çok Yüksek";
}


