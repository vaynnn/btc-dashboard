import streamlit as st
import requests
from pytrends.request import TrendReq

st.set_page_config(page_title="BTC Dashboard", layout="wide")

# ---------------- Custom CSS ----------------
st.markdown(
    """
    <style>
    body {
        background-color: #0E1117;
        color: #E8E8E8;
    }
    .block-container {
        padding: 2rem;
    }
    h1, h2, h3 {
        color: #FF9900; /* Orange accent */
    }
    .stMetric {
        background-color: #1E1E1E;
        border: 1px solid #FF9900;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("BTC Sentiment Dashboard")

# ---------------- Fear & Greed Index ----------------
st.header("Fear & Greed Index")

fgi_url = "https://api.alternative.me/fng/"
fgi_data = requests.get(fgi_url).json()

if "data" in fgi_data:
    fgi_value = fgi_data["data"][0]["value"]
    fgi_class = fgi_data["data"][0]["value_classification"]
    st.metric("Fear & Greed Index", fgi_value, fgi_class)
else:
    st.warning("⚠️ Failed to fetch Fear & Greed data")

# ---------------- Google Trends ----------------
st.header("Google Trends: Bitcoin")

try:
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(["Bitcoin"], timeframe="today 3-m")
    trend_data = pytrends.interest_over_time()
    if not trend_data.empty:
        st.line_chart(trend_data["Bitcoin"])
    else:
        st.warning("⚠️ Failed to fetch Google Trends")
except Exception as e:
    st.error(f"Error Google Trends: {e}")

# ---------------- BlockchainCenter Embeds ----------------
st.header("Altseason Index")
st.components.v1.iframe("https://www.blockchaincenter.net/en/altcoin-season-index/", height=600, scrolling=True)

st.header("Bitcoin Rainbow Chart")
st.components.v1.iframe("https://www.blockchaincenter.net/en/bitcoin-rainbow-chart/", height=600, scrolling=True)

st.header("Crypto Sentiment Index")
st.components.v1.iframe("https://www.blockchaincenter.net/en/crypto-sentiment-index/", height=600, scrolling=True)

st.header("Daily Trending Coins")
st.components.v1.iframe("https://www.blockchaincenter.net/en/coins-trending/", height=600, scrolling=True)
