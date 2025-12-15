import { PriceData, TechnicalIndicators } from "./types";

/**
 * RSI (Relative Strength Index) hesaplama
 * RSI 0-100 arasında bir değerdir
 */
export function calculateRSI(prices: PriceData[], period: number = 14): number {
  if (prices.length < period + 1) {
    return 50; // Yeterli veri yoksa nötr değer
  }

  const closes = prices.map((p) => p.close);
  const gains: number[] = [];
  const losses: number[] = [];

  for (let i = 1; i < closes.length; i++) {
    const change = closes[i] - closes[i - 1];
    gains.push(change > 0 ? change : 0);
    losses.push(change < 0 ? Math.abs(change) : 0);
  }

  // Son period kadar veriyi al
  const recentGains = gains.slice(-period);
  const recentLosses = losses.slice(-period);

  const avgGain = recentGains.reduce((a, b) => a + b, 0) / period;
  const avgLoss = recentLosses.reduce((a, b) => a + b, 0) / period;

  if (avgLoss === 0) return 100;

  const rs = avgGain / avgLoss;
  const rsi = 100 - 100 / (1 + rs);

  return Math.round(rsi * 100) / 100;
}

/**
 * Simple Moving Average (SMA) hesaplama
 */
export function calculateSMA(
  prices: PriceData[],
  period: number
): number {
  if (prices.length < period) {
    return prices[prices.length - 1]?.close || 0;
  }

  const recentPrices = prices.slice(-period);
  const sum = recentPrices.reduce((acc, p) => acc + p.close, 0);
  return Math.round((sum / period) * 100) / 100;
}

/**
 * Volatilite (Risk) hesaplama
 * Standart sapma kullanarak volatiliteyi hesaplar
 */
export function calculateVolatility(
  prices: PriceData[],
  period: number = 20
): number {
  if (prices.length < period) {
    return 0;
  }

  const recentPrices = prices.slice(-period);
  const closes = recentPrices.map((p) => p.close);
  const mean = closes.reduce((a, b) => a + b, 0) / closes.length;

  const variance =
    closes.reduce((acc, price) => acc + Math.pow(price - mean, 2), 0) /
    closes.length;

  const stdDev = Math.sqrt(variance);
  const volatility = (stdDev / mean) * 100; // Yüzde olarak

  return Math.round(volatility * 100) / 100;
}

/**
 * Risk Skoru hesaplama (0-100 arası)
 * Volatilite ve fiyat hareketlerine göre
 */
export function calculateRiskScore(
  prices: PriceData[],
  volatility: number
): number {
  // Volatilite bazlı risk (0-70 puan)
  const volatilityRisk = Math.min(volatility * 2, 70);

  // Son 20 günlük fiyat değişimine göre risk (0-30 puan)
  if (prices.length < 20) {
    return Math.round(volatilityRisk);
  }

  const recent20 = prices.slice(-20);
  const priceChange =
    ((recent20[recent20.length - 1].close - recent20[0].close) /
      recent20[0].close) *
    100;

  const volatilityRisk2 = Math.abs(priceChange) * 0.5;
  const additionalRisk = Math.min(volatilityRisk2, 30);

  const totalRisk = volatilityRisk + additionalRisk;
  return Math.min(Math.round(totalRisk), 100);
}

/**
 * Tüm teknik göstergeleri hesapla
 */
export function calculateAllIndicators(
  prices: PriceData[]
): TechnicalIndicators {
  const rsi = calculateRSI(prices);
  const sma20 = calculateSMA(prices, 20);
  const sma50 = calculateSMA(prices, 50);
  const sma200 = calculateSMA(prices, 200);
  const volatility = calculateVolatility(prices);
  const riskScore = calculateRiskScore(prices, volatility);
  const currentPrice = prices[prices.length - 1]?.close || 0;

  return {
    rsi,
    sma20,
    sma50,
    sma200,
    riskScore,
    volatility,
    currentPrice,
  };
}


