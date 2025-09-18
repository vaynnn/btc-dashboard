import streamlit as st
import requests
import yfinance as yf
from pytrends.request import TrendReq

# Judul
st.title("📊 Bitcoin Macro Dashboard")

# ===== ETF Inflow / Outflow (Coinglass) =====
API_KEY = "ISI_API_KEY_COINGLASS_KAMU"
headers = {"coinglassSecret": API_KEY}
url = "https://open-api.coinglass.com/api/pro/v1/etf/spot/bitcoin/history"
res = requests.get(url, headers=headers).json()
st.subheader("ETF Flows (Last 7 days)")
for d in res["data"][:7]:
    st.write(d["date"], "➡️ Net:", d["netInflow"])

# ===== Fear & Greed Index =====
fg = requests.get("https://api.alternative.me/fng/").json()
fg_value = fg["data"][0]["value"]
fg_text = fg["data"][0]["value_classification"]
st.subheader("Fear & Greed Index")
st.metric("Index", fg_value, fg_text)

# ===== BTC Dominance (CoinGecko) =====
dom = requests.get("https://api.coingecko.com/api/v3/global").json()
btc_dom = dom["data"]["market_cap_percentage"]["btc"]
st.subheader("BTC Dominance")
st.metric("BTC Dominance", f"{btc_dom:.2f}%")

# ===== Google Trends =====
pytrends = TrendReq()
pytrends.build_payload(["Bitcoin"], timeframe="today 3-m")
trends = pytrends.interest_over_time()
st.subheader("Google Search Trend (Bitcoin)")
st.line_chart(trends["Bitcoin"])
