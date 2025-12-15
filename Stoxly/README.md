# 📈 Stoxly - Kişisel Yatırım Kokpiti

Stoxly, karmaşık finansal verileri anlaşılır Türkçe'ye çeviren bir yatırım analiz platformudur.

## 🎯 Özellikler

- **Teknik Analiz**: RSI, Moving Averages, Risk Skoru hesaplama
- **Türkçe Çeviri**: Finansal terimleri anlaşılır Türkçe'ye çevirme
- **Görselleştirme**: İnteraktif grafikler ve dashboard
- **Eğitim**: Finansal terimlerin açıklamaları
- **Borsa İstanbul & Kripto**: Hem hisse senetleri hem de kripto paralar için analiz

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- pip

### Adımlar

1. Projeyi klonlayın veya indirin:
```bash
cd Stoxly
```

2. Sanal ortam oluşturun (önerilir):
```bash
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

## 📖 Kullanım

### Streamlit Uygulaması

Ana uygulamayı çalıştırmak için:

```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak açılacaktır (genellikle http://localhost:8501).

### Jupyter Notebook

Analiz örneklerini görmek için:

```bash
jupyter notebook notebooks/analysis_example.ipynb
```

## 🏗️ Proje Yapısı

```
Stoxly/
├── app.py                      # Streamlit ana uygulama
├── lib/                        # Modüller
│   ├── __init__.py
│   ├── types.py               # Veri yapıları
│   ├── financial_analysis.py  # Teknik göstergeler
│   ├── text_translator.py     # Türkçe çeviri
│   └── mock_service.py        # Veri çekme servisi
├── notebooks/                  # Jupyter notebook'lar
│   └── analysis_example.ipynb
├── requirements.txt            # Python bağımlılıkları
└── README.md
```

## 📊 Kullanım Örnekleri

### Hisse Senedi Analizi

1. Streamlit uygulamasını açın
2. "Varlık Tipi" olarak "Hisse Senedi" seçin
3. Ticker kodunu girin (örn: GARAN, AKBNK, THYAO)
4. "Analiz Et" butonuna tıklayın

### Kripto Para Analizi

1. "Varlık Tipi" olarak "Kripto Para" seçin
2. Ticker kodunu girin (örn: BTC, ETH, ADA)
3. "Analiz Et" butonuna tıklayın

## 🔧 Modüller

### Financial Analysis (`lib/financial_analysis.py`)

- `calculate_rsi()`: RSI hesaplama
- `calculate_sma()`: Moving Average hesaplama
- `calculate_volatility()`: Volatilite hesaplama
- `calculate_risk_score()`: Risk skoru hesaplama
- `calculate_all_indicators()`: Tüm göstergeleri hesaplama

### Text Translator (`lib/text_translator.py`)

- `translate_indicators()`: Göstergeleri Türkçe mesajlara çevirme
- `translate_rsi()`: RSI mesajı
- `translate_risk()`: Risk mesajı
- `translate_trend()`: Trend mesajı
- `get_risk_level()`: Risk seviyesi kategorisi

### Mock Service (`lib/mock_service.py`)

- `fetch_data()`: Ana veri çekme fonksiyonu
- `fetch_stock_data()`: Hisse senedi verisi
- `fetch_crypto_data()`: Kripto para verisi
- `generate_mock_data()`: Mock veri üretme

## 📝 Notlar

- Veri çekme için Yahoo Finance API kullanılmaktadır
- Borsa İstanbul hisseleri için `.IS` suffix'i otomatik eklenir
- İnternet bağlantısı gereklidir (Yahoo Finance API için)
- Veri çekilemezse otomatik olarak mock veri kullanılır

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen pull request gönderin.

## 📄 Lisans

Bu proje eğitim amaçlıdır.

## 📧 İletişim

Sorularınız için issue açabilirsiniz.

---

**Stoxly** - Finansal verileri anlaşılır Türkçe'ye çeviriyoruz! 🇹🇷

