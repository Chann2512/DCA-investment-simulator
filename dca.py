import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Công cụ DCA (Dollar-Cost Averaging)")

# Input từ người dùng
ticker = st.text_input("Nhập mã tài sản (VD: BTC-USD, AAPL)", "BTC-USD")
amount = st.number_input("Số tiền đầu tư mỗi kỳ (USD)", value=100)
freq = st.selectbox("Tần suất", ["1d", "1wk", "1mo"])
start = st.date_input("Ngày bắt đầu", pd.to_datetime("2020-01-01"))
end = st.date_input("Ngày kết thúc")

if st.button("Tính toán"):
    # Lấy dữ liệu giá
    data = yf.download(ticker, start=start, end=end, interval=freq)
    data = data["Close"].dropna()

    # Mô phỏng DCA
    units = []
    total_units = 0
    total_invested = 0

    for date, price in data.items():
        buy_units = amount / price
        total_units += buy_units
        total_invested += amount
        units.append([date, price, buy_units, total_units])

    df = pd.DataFrame(units, columns=["Date", "Price", "Units Bought", "Total Units"])
    if data is None or data.empty:
    st.error("⚠️ Không có dữ liệu cho mã chứng khoán hoặc khoảng thời gian đã nhập.")
    st.stop()
else:
    final_value = total_units * data.iloc[-1]

    # Hiển thị kết quả
    st.subheader("📊 Kết quả")
    st.write(f"Tổng vốn đầu tư: ${total_invested:,.2f}")
    st.write(f"Tổng số lượng tài sản: {total_units:.4f}")
    st.write(f"Giá trị hiện tại: ${final_value:,.2f}")
    st.write(f"Lợi nhuận: {final_value - total_invested:,.2f} USD")

    # Vẽ biểu đồ
    plt.plot(df["Date"], df["Total Units"] * data.values, label="Giá trị DCA")
    plt.plot(data.index, data.values / data.values[0] * total_invested, label="Mua 1 lần")
    plt.legend()

    st.pyplot(plt.gcf())
