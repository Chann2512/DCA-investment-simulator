import streamlit as st
import cryptocompare
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title("📈 DCA Tool for Crypto")

st.markdown("""
This app allows you to **simulate a Dollar-Cost Averaging (DCA) strategy** on cryptocurrencies.  

💡 **How it works:**
- Enter a crypto symbol (e.g., `BTC`, `ETH`, `BNB`).  
- Choose an investment amount and frequency.  
- The app simulates periodic investments (DCA) and compares it with a one-time **Lump Sum** investment.  

📌 **Data source:** [CryptoCompare](https://www.cryptocompare.com/)  
""")

# 👉 Markdown hướng dẫn nhập mã crypto
st.markdown("### 🔹 Enter a cryptocurrency symbol")
st.markdown("Examples: `BTC`, `ETH`, `BNB`, `SOL`, `ADA` ...")

ticker = st.text_input("Crypto symbol", "BTC").upper()
currency = "USD"
amount = st.number_input("💵 Investment per period (USD)", value=100)
freq = st.selectbox("📅 Frequency", ["day", "hour"])  # cryptocompare supports daily/hourly
start = st.date_input("📆 Start date", pd.to_datetime("2020-01-01"))
end = st.date_input("📆 End date")

if st.button("🚀 Run DCA Simulation"):
    # Fetch data
    hist = cryptocompare.get_historical_price_day(
        ticker,
        currency=currency,
        toTs=int(datetime(end.year, end.month, end.day).timestamp())
    )

    if not hist:
        st.error("⚠️ No data available for this crypto. 👉 Try another symbol or date range.")
        st.stop()

    data = pd.DataFrame(hist)
    data["time"] = pd.to_datetime(data["time"], unit="s")
    data = data.set_index("time")
    data = data[(data.index >= pd.to_datetime(start)) & (data.index <= pd.to_datetime(end))]
    data = data["close"]

    if data.empty:
        st.error("⚠️ No data in this date range. 👉 Please choose another time period.")
        st.stop()

    # DCA simulation
    units = []
    total_units, total_invested = 0, 0
    for date, price in data.items():
        buy_units = amount / price
        total_units += buy_units
        total_invested += amount
        units.append([date, price, buy_units, total_units])

    df = pd.DataFrame(units, columns=["Date", "Price", "Units Bought", "Total Units"])
    final_value = total_units * data.iloc[-1]

    # Results
    st.subheader("📊 Results")
    st.write(f"**Total Invested:** ${total_invested:,.2f}")
    st.write(f"**Total Units:** {total_units:.4f} {ticker}")
    st.write(f"**Final Value:** ${final_value:,.2f}")
    st.write(f"**Profit:** {final_value - total_invested:,.2f} USD")

    # Chart
    plt.style.use("dark_background")  
    plt.figure(figsize=(10, 5), facecolor="#0e1117")  
    ax = plt.gca()
    ax.set_facecolor("#0a0f1f") 
    
    # Vẽ DCA Value màu cyan
    plt.plot(df["Date"], df["Total Units"] * data.values, 
             label="DCA Value", color="cyan", linewidth=2)
    
    # Vẽ Lump Sum màu vàng
    plt.plot(data.index, data.values / data.values[0] * total_invested, 
             label="Lump Sum", color="yellow", linewidth=2)
    
    plt.title(f"DCA vs Lump Sum for {ticker}", color="white")
    plt.xlabel("Date", color="white")
    plt.ylabel("Portfolio Value (USD)", color="white")
    
    plt.legend(facecolor="#0a0f1f", edgecolor="white", labelcolor="white")
    plt.tick_params(colors="white")
    
    st.pyplot(plt.gcf())

