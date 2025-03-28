import time
import matplotlib.pyplot as plt
from MA.SMA import SMA
from MA.EMA import EMA
from test_price import testSOL

def SpotTestSMA(price_data):
    print("Тест SMA")
    sma_indicator = SMA()
    data_test, data_train = price_data[:100], price_data[100:]
    
    top_result, top_short, top_long = 0, 0, 0

    for window_long in range(20, 201, 20):
        for window_short in range(5, 26, 5):
            sma_indicator.get_updata(window_short=window_short, window_long=window_long, data_price=data_test)

            buy_price = 0
            history_price = []
            for price in data_train:
                indicator = sma_indicator.calculate_sma(price)
                # print(f"Indicator: {indicator} | Price: {price}")
                if indicator == "Buy" and buy_price == 0:
                    buy_price = price
                elif indicator == "Sell" and buy_price != 0:
                    history_price.append(["sell", buy_price, price, price - buy_price])
                    buy_price = 0
                # Условие для тейк-профита (фиксируем прибыль при +5%)
                elif buy_price != 0 and price >= buy_price * 1.05:
                    history_price.append(["take_profit", buy_price, price, round(price - buy_price, 2)])
                    buy_price = 0
                # Условие для стоп-лосса (фиксируем убыток при -5%)
                elif buy_price != 0 and price <= buy_price * 0.95:
                    history_price.append(["stop_loss", buy_price, price, round(price - buy_price, 2)])
                    buy_price = 0
            
            result_price = 0
            for i in history_price:
                # print(f"Причина: {i[0]} | Цена покупки: {i[1]} | Цена продажи: {i[2]} | Разница: {i[3]}")
                result_price+=i[3]
            print(f"Итог: {result_price} | Окно Short: {window_short} | Окно Long: {window_long}")
            if top_result<result_price:
                top_result, top_short, top_long = result_price, window_short, window_long
    print(f"Лучшая комбинация short: {top_short} | long: {top_long}. Прибыль: {top_result}")


def testEMA(price_data):
    print("Тест EMA")
    ema_indicator = EMA()
    data_test, data_train = price_data[:100], price_data[100:]

    top_result, top_short, top_long = 0, 0, 0

    for window_long in range(20, 201, 20):
        for window_short in range(5, 26, 5):
            ema_indicator.get_updata(window_short=window_short, window_long=window_long, data_price=data_test)

            buy_price = 0
            history_price = []
            for price in data_train:
                indicator = ema_indicator.calculator_ema(price)
                # print(f"Indicator: {indicator} | Price: {price}")
                if indicator == "Buy" and buy_price == 0:
                    buy_price = price
                elif indicator == "Sell" and buy_price != 0:
                    history_price.append(["sell", buy_price, price, price - buy_price])
                    buy_price = 0
                # Условие для тейк-профита (фиксируем прибыль при +5%)
                elif buy_price != 0 and price >= buy_price * 1.05:
                    history_price.append(["take_profit", buy_price, price, round(price - buy_price, 2)])
                    buy_price = 0
                # Условие для стоп-лосса (фиксируем убыток при -5%)
                elif buy_price != 0 and price <= buy_price * 0.95:
                    history_price.append(["stop_loss", buy_price, price, round(price - buy_price, 2)])
                    buy_price = 0
            
            result_price = 0
            for i in history_price:
                # print(f"Причина: {i[0]} | Цена покупки: {i[1]} | Цена продажи: {i[2]} | Разница: {i[3]}")
                result_price+=i[3]
            print(f"Итог: {result_price} | Окно Short: {window_short} | Окно Long: {window_long}")
            if top_result<result_price:
                top_result, top_short, top_long = result_price, window_short, window_long
    print(f"Лучшая комбинация short: {top_short} | long: {top_long}. Прибыль: {top_result}")


def main():
    test_price = testSOL()
    # SpotTestSMA(test_price)
    testEMA(test_price)

if __name__ == "__main__":
    main()