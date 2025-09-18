import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq

st.set_page_config(page_title="BTC Sentiment Dashboard", layout="wide")

st.title("📊 BTC Sentiment Dashboard (Free, No API Key)")

# ---------------- Fear & Greed Index ----------------
st.subheader("😨 Fear & Greed Index (Crypto Market Sentiment)")

fgi_url = "https://api.alternative.me/fng/"
fgi_data = requests.get(fgi_url).json()

if "data" in fgi_data:
    fgi_value = fgi_data["data"][0]["value"]
    fgi_class = fgi_data["data"][0]["value_classification"]
    st.metric("Fear & Greed Index", fgi_value, fgi_class)
else:
    st.warning("⚠️ Gagal fetch Fear & Greed data")

# ---------------- Google Trends ----------------
st.subheader("📈 Google Trends: Bitcoin")

pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(["Bitcoin"], timeframe="today 3-m")

trend_data = pytrends.interest_over_time()

if not trend_data.empty:
    st.line_chart(trend_data["Bitcoin"])
else:
    st.warning("⚠️ Gagal fetch Google Trends")

# ---------------- Altseason Index ----------------
st.subheader("🪙 Altseason Index")

alt_url = "https://www.blockchaincenter.net/en/altcoin-season-index/"
st.markdown(f"[Klik di sini untuk lihat Altseason Index Live]({alt_url})")

try:
    st.components.v1.iframe(alt_url, height=600, scrolling=True)
except:
    st.warning("⚠️ Tidak bisa load Altseason Index embed")
