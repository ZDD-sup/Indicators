from test_price import testSOL
import time
import matplotlib.pyplot as plt

from moment_indicators.RSI import RSI
from MA.SMA import SMA
from MA.EMA import EMA
from MA.SMA_EMA import SEMA
from MA.WMA import WMA

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

def testSEMA(price_data):
    print("Тест SEMA")
    sema_indicator = SEMA()
    data_test, data_train = price_data[:100], price_data[100:]

    top_result, top_short, top_long = 0, 0, 0

    for window_long in range(20, 201, 20):
        for window_short in range(5, 26, 5):
            sema_indicator.get_update_sema(window_short=window_short, window_long=window_long, data_price=data_test)

            buy_price = 0
            history_price = []
            for price in data_train:
                indicator = sema_indicator.calculator_sema(price)
                # if indicator!= "Neutral":
                #     print(f"Indicator: {indicator} | Price: {price}")
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

def testWMA(price_data):
    print("Тест WMA")
    wma_indicator = WMA()
    data_test, data_train = price_data[:100], price_data[100:]

    top_result, top_short, top_long = 0, 0, 0

    for window_long in range(20, 201, 20):
        for window_short in range(5, 26, 5):
            wma_indicator.startWMA(window_short, window_long, data_test)

            buy_price = 0
            history_price = []
            for price in data_train:
                indicator = wma_indicator.calculator_wma(price)
                # if indicator!= "Neutral":
                #     print(f"Indicator: {indicator} | Price: {price}")
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
    # testEMA(test_price)
    # testSEMA(test_price)
    # testWMA(test_price)
    testRSI(test_price)

if __name__ == "__main__":
    main()
