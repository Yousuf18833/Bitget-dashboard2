
# Bitget BTC Regional Tracker - Streamlit Dashboard

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Bitget BTC Dashboard", layout="wide")
st.title("📊 Bitget Bitcoin Buying/Selling Tracker")

# --- Section 1: Real-time BTC Price from CoinGecko ---
with st.container():
    st.subheader("🔄 Real-time Bitcoin Price")
    coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        price_data = requests.get(coingecko_url).json()
        btc_price = price_data['bitcoin']['usd']
        st.metric(label="BTC/USDT Price", value=f"${btc_price:,.2f}")
    except:
        st.error("Failed to fetch BTC price.")

# --- Section 2: Simulated Region-wise Volume ---
with st.container():
    st.subheader("🌍 Approximate Region-wise Trading Volume (Simulated Data)")

    # Simulated volume data - ideally you'd use Bitget + analytics APIs
    region_data = {
        'Country': ['United States', 'South Korea', 'Germany', 'Brazil', 'Thailand', 'Australia'],
        'Buy Volume (BTC)': [1240, 890, 670, 430, 550, 300],
        'Sell Volume (BTC)': [980, 720, 610, 390, 480, 260]
    }
    df_region = pd.DataFrame(region_data)
    st.dataframe(df_region)

    fig = px.bar(df_region, x='Country', y=['Buy Volume (BTC)', 'Sell Volume (BTC)'],
                 title="Regional Buy vs Sell Volume", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

# --- Section 3: Whale Alert API (Large Transactions) ---
with st.container():
    st.subheader("🐋 Recent Large BTC Transfers (Whale Alert)")
    whale_api_url = "https://api.whale-alert.io/v1/transactions"
    params = {
        'api_key': 'YOUR_WHALE_ALERT_API_KEY',  # <-- Replace with real key
        'currency': 'btc',
        'min_value': 500000,  # USD
        'limit': 5
    }
    try:
        response = requests.get(whale_api_url, params=params)
        whale_data = response.json()['transactions']

        for tx in whale_data:
            st.write(f"🔁 {tx['amount']} BTC | {tx['from']['owner']} ➝ {tx['to']['owner']} | Value: ${tx['amount_usd']:,} at {datetime.fromtimestamp(tx['timestamp'])}")
    except:
        st.warning("Could not fetch whale alerts. Use your API key.")

# --- Section 4: BTC News Headlines (Optional) ---
with st.container():
    st.subheader("📰 Latest Bitcoin News")
    news_api = "https://cryptopanic.com/api/v1/posts/?auth_token=YOUR_NEWS_API_KEY&currencies=BTC"
    try:
        news = requests.get(news_api).json()['results'][:5]
        for article in news:
            st.write(f"[{article['title']}]({article['url']})")
    except:
        st.info("Connect a news API (e.g., CryptoPanic) to show news.")
