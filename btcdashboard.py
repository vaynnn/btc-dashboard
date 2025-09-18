import streamlit as st
import requests
import pandas as pd
from pytrends.request import TrendReq

st.set_page_config(page_title="BTC Dashboard", layout="wide")
st.title("📊 Bitcoin Dashboard")

# ==================== Coinglass ====================
st.subheader("Derivatives & ETF (Coinglass)")

COINGLASS_KEY = st.secrets["coinglass_secret"]
cg_headers = {"coinglassSecret": COINGLASS_KEY}

# daftar endpoint coinglass
coinglass_indicators = {
    "ETF Flows": "etf/spot/bitcoin/history",
    "Funding Rate": "futures/funding_rates_chart?symbol=BTC",
    "Open Interest": "futures/open_interest_chart?symbol=BTC",
    "Liquidations": "futures/liquidation_chart?symbol=BTC",
}

cg_choice = st.selectbox("Pilih indikator Coinglass:", list(coinglass_indicators.keys()))
cg_url = f"https://open-api.coinglass.com/api/pro/v1/{coinglass_indicators[cg_choice]}"

try:
    res = requests.get(cg_url, headers=cg_headers).json()
    if "data" in res and res["data"]:
        df = pd.DataFrame(res["data"])
        if "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"], unit="ms", errors="coerce")
            df = df.set_index("time")
        st.line_chart(df[df.columns[-1]])
    else:
        st.warning(f"Tidak ada data Coinglass ({cg_choice})")
except Exception as e:
    st.error(f"Coinglass error: {e}")

# ==================== Fear & Greed ====================
st.subheader("Fear & Greed Index")
try:
    fg = requests.get("https://api.alternative.me/fng/").json()
    if "data" in fg:
        fg_value = fg["data"][0]["value"]
        fg_text = fg["data"][0]["value_classification"]
        st.metric("Fear & Greed", fg_value, fg_text)
    else:
        st.warning("Tidak ada data Fear & Greed")
except Exception as e:
    st.error(f"FGI error: {e}")

# ==================== BTC Dominance ====================
st.subheader("BTC Dominance (CoinGecko)")
try:
    dom = requests.get("https://api.coingecko.com/api/v3/global").json()
    if "data" in dom:
        btc_dom = dom["data"]["market_cap_percentage"]["btc"]
        st.metric("BTC Dominance", f"{btc_dom:.2f}%")
    else:
        st.warning("Tidak ada data Dominance")
except Exception as e:
    st.error(f"Dominance error: {e}")

# ==================== Google Trends ====================
st.subheader("Google Trends: Bitcoin (3 bulan terakhir)")
try:
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(["Bitcoin"], timeframe="today 3-m")
    trends = pytrends.interest_over_time()
    if not trends.empty:
        st.line_chart(trends["Bitcoin"])
    else:
        st.warning("Data Google Trends kosong")
except Exception as e:
    st.error(f"Google Trends error: {e}")

# ==================== Altseason Index ====================
st.subheader("Altseason Index (BlockchainCenter)")
try:
    alt = requests.get("https://blockchaincenter.net/api/altseason").json()
    if "altseason_index" in alt:
        st.metric("Altseason Index", alt["altseason_index"])
    else:
        st.warning("Tidak ada data Altseason")
except Exception as e:
    st.error(f"Altseason error: {e}")

# ==================== CryptoQuant ====================
st.subheader("On-chain Indicators (CryptoQuant)")

CQ_KEY = st.secrets["cryptoquant_secret"]
cq_headers = {"Authorization": f"Bearer {CQ_KEY}"}

cq_indicators = {
    "MVRV Z-Score": "indicators/mvrv-zscore",
    "Exchange Reserves": "indicators/exchange-reserve",
    "Miner Outflow": "indicators/miner-outflow",
    "Stablecoin Supply Ratio": "indicators/stablecoin-supply-ratio",
    "SOPR": "indicators/sopr",
    "NUPL": "indicators/nupl",
}

cq_choice = st.selectbox("Pilih indikator CryptoQuant:", list(cq_indicators.keys()))
cq_url = f"https://api.cryptoquant.com/v1/btc/{cq_indicators[cq_choice]}"

try:
    res = requests.get(cq_url, headers=cq_headers).json()
    if "result" in res and "data" in res["result"]:
        df = pd.DataFrame(res["result"]["data"])
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df.set_index("date")
        st.line_chart(df[df.columns[-1]])
    else:
        st.warning(f"Tidak ada data CryptoQuant ({cq_choice})")
except Exception as e:
    st.error(f"CryptoQuant error: {e}")
