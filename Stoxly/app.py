"""
Stoxly - Kişisel Yatırım Kokpiti
Streamlit ana uygulama
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from lib.mock_service import fetch_data
from lib.financial_analysis import calculate_all_indicators
from lib.text_translator import translate_indicators, get_risk_level
from lib.types import AssetType, AnalysisResult

# Sayfa yapılandırması
st.set_page_config(
    page_title="Stoxly - Kişisel Yatırım Kokpiti",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .action-box {
        background-color: #d1ecf1;
        border: 2px solid #0dcaf0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown('<h1 class="main-header">📈 Stoxly - Kişisel Yatırım Kokpiti</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Kullanıcı girişi
with st.sidebar:
    st.header("🔍 Analiz Ayarları")
    
    asset_type = st.selectbox(
        "Varlık Tipi",
        ["stock", "crypto"],
        format_func=lambda x: "Hisse Senedi" if x == "stock" else "Kripto Para"
    )
    
    if asset_type == "stock":
        ticker = st.text_input(
            "Hisse Kodu",
            value="GARAN",
            help="Borsa İstanbul hisse kodu (örn: GARAN, AKBNK, THYAO)"
        )
    else:
        ticker = st.text_input(
            "Kripto Kodu",
            value="BTC",
            help="Kripto para kodu (örn: BTC, ETH, ADA)"
        )
    
    analyze_button = st.button("📊 Analiz Et", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 💡 Bilgi")
    st.info("""
    Stoxly, karmaşık finansal verileri 
    anlaşılır Türkçe'ye çeviren bir 
    yatırım analiz platformudur.
    """)

# Para birimi fonksiyonu
def get_currency(asset_type: AssetType) -> str:
    """Asset type'a göre para birimini döndür"""
    return "USD" if asset_type == "crypto" else "TL"

def get_currency_symbol(asset_type: AssetType) -> str:
    """Asset type'a göre para birimi sembolünü döndür"""
    return "$" if asset_type == "crypto" else "TL"

# Ana içerik
if analyze_button or 'analysis_result' in st.session_state:
    if analyze_button:
        with st.spinner("Veriler çekiliyor ve analiz ediliyor..."):
            # Veri çekme
            price_data = fetch_data(ticker, asset_type)
            
            if not price_data:
                st.error("Veri çekilemedi. Lütfen ticker kodunu kontrol edin.")
                st.stop()
            
            # Analiz
            indicators = calculate_all_indicators(price_data)
            translated_insights = translate_indicators(indicators)
            risk_level = get_risk_level(indicators.risk_score)
            
            analysis_result = AnalysisResult(
                indicators=indicators,
                translated_insights=translated_insights,
                risk_level=risk_level
            )
            
            st.session_state['analysis_result'] = analysis_result
            st.session_state['price_data'] = price_data
            st.session_state['ticker'] = ticker
            st.session_state['asset_type'] = asset_type
    
    if 'analysis_result' in st.session_state:
        analysis_result = st.session_state['analysis_result']
        price_data = st.session_state['price_data']
        ticker = st.session_state['ticker']
        asset_type = st.session_state['asset_type']
        
        indicators = analysis_result.indicators
        insights = analysis_result.translated_insights
        
        # Dashboard Layout
        # Sol Panel - Uyarılar ve Aksiyonlar
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### ⚠️ Ana Uyarı ve Aksiyon")
            
            # Ana Uyarı
            if insights.main_warning:
                warning_color = "🔴" if "Yüksek" in insights.main_warning or "Aşırı" in insights.main_warning else "🟡"
                st.markdown(f"""
                <div class="warning-box">
                    <h3>{warning_color} {insights.main_warning}</h3>
                </div>
                """, unsafe_allow_html=True)
            
            # Ana Aksiyon
            if insights.main_action:
                st.markdown(f"""
                <div class="action-box">
                    <h4>💡 Öneri: {insights.main_action}</h4>
                </div>
                """, unsafe_allow_html=True)
            
            # RSI Mesajı
            st.markdown("### 📊 RSI Analizi")
            rsi_color = "🔴" if indicators.rsi >= 70 else "🟢" if indicators.rsi <= 30 else "🟡"
            st.info(f"{rsi_color} **RSI: {indicators.rsi:.2f}**\n\n{insights.rsi_message}")
            
            # Risk Mesajı
            st.markdown("### ⚖️ Risk Analizi")
            risk_colors = {
                "Düşük": "🟢",
                "Orta": "🟡",
                "Yüksek": "🟠",
                "Çok Yüksek": "🔴"
            }
            risk_emoji = risk_colors.get(analysis_result.risk_level, "⚪")
            st.warning(f"{risk_emoji} **Risk Seviyesi: {analysis_result.risk_level}** ({indicators.risk_score:.1f}/100)\n\n{insights.risk_message}")
            
            # Trend Mesajı
            st.markdown("### 📈 Trend Analizi")
            st.success(f"**{insights.trend_message}**")
        
        with col2:
            st.markdown("### 📊 Fiyat Grafiği")
            
            # Grafik oluştur
            dates = [p.date for p in price_data]
            closes = [p.close for p in price_data]
            highs = [p.high for p in price_data]
            lows = [p.low for p in price_data]
            
            # Candlestick grafik
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=('Fiyat Hareketi', 'Hacim'),
                row_width=[0.7, 0.3]
            )
            
            # Candlestick
            fig.add_trace(
                go.Candlestick(
                    x=dates,
                    open=[p.open for p in price_data],
                    high=highs,
                    low=lows,
                    close=closes,
                    name="Fiyat"
                ),
                row=1, col=1
            )
            
            # Moving Averages
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=[indicators.sma20] * len(dates),
                    name="SMA 20",
                    line=dict(color='blue', width=1, dash='dash')
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=[indicators.sma50] * len(dates),
                    name="SMA 50",
                    line=dict(color='orange', width=1, dash='dash')
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=[indicators.sma200] * len(dates),
                    name="SMA 200",
                    line=dict(color='red', width=1, dash='dash')
                ),
                row=1, col=1
            )
            
            # Hacim
            volumes = [p.volume for p in price_data]
            fig.add_trace(
                go.Bar(
                    x=dates,
                    y=volumes,
                    name="Hacim",
                    marker_color='lightblue'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                height=600,
                showlegend=True,
                xaxis_rangeslider_visible=False,
                title=f"{ticker} - Son 1 Yıl Fiyat Analizi"
            )
            
            currency = get_currency(asset_type)
            fig.update_xaxes(title_text="Tarih", row=2, col=1)
            fig.update_yaxes(title_text=f"Fiyat ({currency})", row=1, col=1)
            fig.update_yaxes(title_text="Hacim", row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Alt Panel - Detaylı Metrikler
        st.markdown("---")
        st.markdown("### 📋 Detaylı Metrikler")
        
        col3, col4, col5, col6, col7 = st.columns(5)
        
        currency_symbol = get_currency_symbol(asset_type)
        currency = get_currency(asset_type)
        
        with col3:
            st.metric("Güncel Fiyat", f"{currency_symbol}{indicators.current_price:.2f}")
        
        with col4:
            st.metric("RSI", f"{indicators.rsi:.2f}")
        
        with col5:
            st.metric("Volatilite", f"%{indicators.volatility:.2f}")
        
        with col6:
            st.metric("Risk Skoru", f"{indicators.risk_score:.1f}/100")
        
        with col7:
            st.metric("SMA 20", f"{currency_symbol}{indicators.sma20:.2f}")
        
        # Eğitimsel Tooltip'ler
        st.markdown("---")
        st.markdown("### 📚 Terimler Açıklaması")
        
        with st.expander("RSI (Relative Strength Index) Nedir?"):
            st.write("""
            RSI, bir varlığın aşırı alım veya aşırı satım durumunu gösteren bir göstergedir.
            - **70-100 arası**: Aşırı alım (Overbought) - Fiyat çok yükselmiş olabilir
            - **30-70 arası**: Normal bölge
            - **0-30 arası**: Aşırı satım (Oversold) - Fiyat çok düşmüş olabilir
            """)
        
        with st.expander("Moving Average (Hareketli Ortalama) Nedir?"):
            st.write("""
            Hareketli ortalama, belirli bir dönemdeki ortalama fiyatı gösterir.
            - **SMA 20**: Son 20 günün ortalaması (kısa vade)
            - **SMA 50**: Son 50 günün ortalaması (orta vade)
            - **SMA 200**: Son 200 günün ortalaması (uzun vade)
            
            Fiyat ortalamaların üzerindeyse yükseliş, altındaysa düşüş trendi olabilir.
            """)
        
        with st.expander("Volatilite ve Risk Skoru Nedir?"):
            st.write("""
            - **Volatilite**: Fiyatın ne kadar değişken olduğunu gösterir. Yüksek volatilite = daha fazla risk
            - **Risk Skoru**: Varlığın genel risk seviyesini 0-100 arasında gösterir
            - Düşük risk = Daha güvenli yatırım
            - Yüksek risk = Daha fazla kazanç potansiyeli ama daha fazla kayıp riski
            """)
        
else:
    # Hoş geldiniz ekranı
    st.info("👈 Sol taraftaki panelden bir varlık seçin ve analiz butonuna tıklayın.")
    
    st.markdown("""
    ### 🎯 Stoxly Nedir?
    
    Stoxly, karmaşık finansal verileri anlaşılır Türkçe'ye çeviren bir yatırım analiz platformudur.
    
    **Özellikler:**
    - 📊 Teknik analiz göstergeleri (RSI, Moving Averages)
    - ⚠️ Risk değerlendirmesi
    - 📈 Görsel grafikler
    - 🇹🇷 Türkçe açıklamalar
    - 📚 Eğitici içerikler
    
    **Nasıl Kullanılır?**
    1. Sol panelden varlık tipini seçin (Hisse Senedi veya Kripto Para)
    2. Ticker kodunu girin (örn: GARAN, BTC)
    3. "Analiz Et" butonuna tıklayın
    4. Sonuçları inceleyin!
    """)

