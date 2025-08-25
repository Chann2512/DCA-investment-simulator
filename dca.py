import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# App Title
st.title("📈 DCA (Dollar-Cost Averaging) Simulator")

# Description
st.markdown("""
This app simulates the **Dollar-Cost Averaging (DCA)** investment strategy.  
You can use it for **cryptocurrencies** (e.g., BTC-USD, ETH-USD), **stocks** (e.g., AAPL, TSLA), **ETFs** (e.g., SPY, QQQ), or even **forex/commodities** available on Yahoo Finance.  

💡 With DCA, you invest a fixed amount of money at regular intervals, regardless of price.  
This strategy reduces the impact of volatility and avoids trying to "time the market".
""")

# User inputs
ticker = st.text_input("Enter asset ticker (e.g., BTC-USD, AAPL)", "BTC-USD")
amount = st.number_input("Investment amount per period (USD)", value=100)
freq = st.selectbox("Investment frequency", ["1d", "1wk", "1mo"])
start = st.date_input("Start date", pd.to_datetime("2020-01-01"))
end = st.date_input("End date")

if st.button("Run Simulation"):
    # Fetch price data
    data = yf.download(ticker, start=start, end=end, interval=freq)
    
    if data is None or data.empty:
        st.error("⚠️ No data available for this ticker or time range.")
        st.stop()

    data = data["Close"].dropna()

    # Simulate DCA
    units = []
    total_units = 0
    total_invested = 0

    for date, price in data.items():
        buy_units = amount / price
        total_units += buy_units
        total_invested += amount
        units.append([date, price, buy_units, total_units])

    df = pd.DataFrame(units, columns=["Date", "Price", "Units Bought", "Total Units"])
    final_value = total_units * data.iloc[-1]

    # Results
    st.subheader("📊 Results")
    st.write(f"Total invested capital: **${total_invested:,.2f}**")
    st.write(f"Total units accumulated: **{total_units:.4f}**")
    st.write(f"Current portfolio value: **${final_value:,.2f}**")
    st.write(f"Profit/Loss: **${final_value - total_invested:,.2f} USD**")

    # Chart
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["Total Units"] * data.values, label="DCA Strategy")
    plt.plot(data.index, data.values / data.values[0] * total_invested, label="Lump-Sum Investment")
    plt.legend()
    plt.title(f"DCA Simulation for {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value (USD)")
    st.pyplot(plt.gcf())
