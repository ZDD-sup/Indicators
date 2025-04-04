from moment_indicators.RSI import RSI
from test_price import testSOL

def testRSI(price_data):
    data_test, data_train = price_data[:100], price_data[100:]

    indicator_rsi = RSI()

    indicator_rsi.initialize_rsi(14, data_train)

    for price in data_test:
        rsi_value = indicator_rsi.update_price(price)
        if rsi_value>=70:
            print(f"Возможно падение. Рынок перекуплен RSI: {rsi_value:.2f}")
        elif rsi_value<=30:
            print(f"Возможен рост. Рынок перепродан RSI: {rsi_value:.2f}")

def main():
    test_price = testSOL()
    testRSI(test_price)

if __name__ == "__main__":
    main()

