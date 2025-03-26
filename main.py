import time
from MA.SMA import SMA

def testSMA():
    print("Тест SMA")
    # Задаем размеры окон скользящих средних
    window_short = 3
    window_long = 7

    # Задаем список начальных цен
    initial_prices = [10.5, 12, 15.3, 13, 16.8, 14, 17.1, 19, 18.5, 20]

    starttime = time.time()
    # Создаем экземпляр класса SMA с начальными ценами
    sma_indicator = SMA(window_short=window_short, window_long=window_long, data_price=initial_prices)

    print(f"Начальные цены: {initial_prices}")

    # Задаем 10 новых цен для добавления
    new_prices = [22.2, 21, 10, 25, 24.9, 26, 28.4, 27, 29.1, 30]

    print("\nДобавление новых цен и сигналы:")
    for price in new_prices:
        signal = sma_indicator.calculate_sma(price)
        print(f"Новая цена: {price}, Сигнал: {signal}")

    print(f"\nИстория всех цен: {sma_indicator.data_price}")
    endtime = time.time()
    print(f"Время выполнения: {endtime-starttime}")

def main():
    testSMA()

if __name__ == "__main__":
    main()