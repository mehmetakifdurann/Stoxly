export interface PriceData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface TechnicalIndicators {
  rsi: number;
  sma20: number;
  sma50: number;
  sma200: number;
  riskScore: number;
  volatility: number;
  currentPrice: number;
}

export interface AnalysisResult {
  indicators: TechnicalIndicators;
  translatedInsights: TranslatedInsights;
  riskLevel: "Düşük" | "Orta" | "Yüksek" | "Çok Yüksek";
}

export interface TranslatedInsights {
  rsiMessage: string;
  riskMessage: string;
  trendMessage: string;
  mainWarning?: string;
  mainAction?: string;
}

export type AssetType = "stock" | "crypto";

export interface Asset {
  ticker: string;
  name: string;
  type: AssetType;
}


