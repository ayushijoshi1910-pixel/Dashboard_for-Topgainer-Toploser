import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Indian Stock Market Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Live Indian Stock Market Dashboard")

st.write(
    "Track Top Gainers, Top Losers, and Volume Leaders using live market data."
)

# ---------------------------------------------------
# STOCK LIST
# ---------------------------------------------------

stocks = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "SBI": "SBIN.NS",
    "ITC": "ITC.NS",
    "Wipro": "WIPRO.NS",
    "Adani Enterprises": "ADANIENT.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Axis Bank": "AXISBANK.NS",
    "Kotak Bank": "KOTAKBANK.NS",
    "LT": "LT.NS",
    "Maruti": "MARUTI.NS",
    "Asian Paints": "ASIANPAINT.NS"
}

# ---------------------------------------------------
# FETCH LIVE MARKET DATA
# ---------------------------------------------------

market_data = []

with st.spinner("Fetching live market data..."):

    for company, ticker in stocks.items():

        try:

            data = yf.download(
                ticker,
                period="5d",
                interval="1d",
                auto_adjust=True,
                progress=False
            )

            # ---------------------------------------------------
            # FIX MULTI-INDEX COLUMNS
            # ---------------------------------------------------

            if isinstance(data.columns, pd.MultiIndex):

                data.columns = (
                    data.columns.get_level_values(0)
                )

            data.reset_index(inplace=True)

            # ---------------------------------------------------
            # CHECK DATA
            # ---------------------------------------------------

            if len(data) >= 2:

                previous_close = float(
                    data["Close"].iloc[-2]
                )

                current_close = float(
                    data["Close"].iloc[-1]
                )

                latest_volume = int(
                    data["Volume"].iloc[-1]
                )

                percent_change = (
                    (
                        current_close - previous_close
                    )
                    / previous_close
                ) * 100

                market_data.append({

                    "Company": company,

                    "Ticker": ticker,

                    "Close": round(
                        current_close,
                        2
                    ),

                    "Change %": round(
                        percent_change,
                        2
                    ),

                    "Volume": latest_volume
                })

        except Exception as e:

            st.warning(
                f"Error loading {company}: {e}"
            )

# ---------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------

df = pd.DataFrame(market_data)

# ---------------------------------------------------
# HANDLE EMPTY DATA
# ---------------------------------------------------

if df.empty:

    st.error(
        "No stock data available."
    )

else:

    # ---------------------------------------------------
    # TOP GAINERS
    # ---------------------------------------------------

    top_gainers = (

        df.sort_values(
            by="Change %",
            ascending=False
        )

        .head(5)
    )

    # ---------------------------------------------------
    # TOP LOSERS
    # ---------------------------------------------------

    top_losers = (

        df.sort_values(
            by="Change %",
            ascending=True
        )

        .head(5)
    )

    # ---------------------------------------------------
    # VOLUME LEADERS
    # ---------------------------------------------------

    volume_leaders = (

        df.sort_values(
            by="Volume",
            ascending=False
        )

        .head(5)
    )

    # ---------------------------------------------------
    # MARKET SUMMARY
    # ---------------------------------------------------

    st.subheader("📌 Market Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Stocks Tracked",
        len(df)
    )

    col2.metric(
        "Top Gainer",
        top_gainers.iloc[0]["Company"]
    )

    col3.metric(
        "Highest Volume",
        volume_leaders.iloc[0]["Company"]
    )

    # ---------------------------------------------------
    # TOP GAINERS
    # ---------------------------------------------------

    st.subheader("🚀 Top Gainers")

    st.dataframe(top_gainers)

    fig1 = px.bar(
        top_gainers,
        x="Company",
        y="Change %",
        title="Top Gainers"
    )

    st.plotly_chart(
        fig1,
        width="stretch"
    )

    # ---------------------------------------------------
    # TOP LOSERS
    # ---------------------------------------------------

    st.subheader("📉 Top Losers")

    st.dataframe(top_losers)

    fig2 = px.bar(
        top_losers,
        x="Company",
        y="Change %",
        title="Top Losers"
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

    # ---------------------------------------------------
    # VOLUME LEADERS
    # ---------------------------------------------------

    st.subheader("📊 Volume Leaders")

    st.dataframe(volume_leaders)

    fig3 = px.bar(
        volume_leaders,
        x="Company",
        y="Volume",
        title="Highest Trading Volume"
    )

    st.plotly_chart(
        fig3,
        width="stretch"
    )

    # ---------------------------------------------------
    # COMPLETE MARKET DATA
    # ---------------------------------------------------

    st.subheader("📋 Complete Market Data")

    st.dataframe(df)

    # ---------------------------------------------------
    # FOOTER
    # ---------------------------------------------------

    st.info(
        "Live market data fetched using Yahoo Finance API."
    )
