import time
import matplotlib.pyplot as plt
from MA.SMA import SMA
from MA.EMA import EMA

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

def testEMA():
    print("Тест EMA")
    # Пример исторических данных (цены)
    data_price = [100.5 , 102, 105, 108, 107, 110, 115.1, 118, 120, 125]
    starttime = time.time()
    # Создаем объект класса EMA
    ema = EMA()

    # Инициализация с коротким и длинным периодами, а также историческими данными
    ema.get_updata(window_short=3, window_long=5, data_price=data_price)

    # Тестирование расчетов EMA с новыми поступающими ценами
    new_prices = [126, 127, 124, 122.2, 121, 119, 118, 117.9, 116]
    list_short_1 = []
    list_long_1 = []
    # Вывод торговых сигналов для каждой новой цены
    for price in new_prices:
        signal = ema.calculator_ema(price)
        list_short_1.append(ema.previous_EMA_short)
        list_long_1.append(ema.previous_EMA_long)
        print(f"Цена: {price}, Сигнал: {signal}")

    # x1 = range(len(data_price))
    # x2 = [i + 3 for i in range(len(list_short_1))]
    # x3 = [i + 5 for i in range(len(list_long_1))]
    # # Построение графика
    # plt.figure(figsize=(10, 6))  # Устанавливаем размер графика (необязательно)

    # plt.plot(x1, data_price, label='price', marker='o')
    # plt.plot(x2, list_short_1, label='short (начинается с индекса {})'.format(3), marker='x')
    # plt.plot(x3, list_long_1, label='long (начинается с индекса {})'.format(5), marker='s')

    # # Добавление подписей к осям и заголовка
    # plt.xlabel('Индекс')
    # plt.ylabel('Значение')
    # plt.title('График трех списков')

    # # Добавление легенды
    # plt.legend()

    # # Включение сетки (необязательно)
    # plt.grid(True)

    # # Отображение графика
    # plt.show()

    # Пример обновления данных с изменением окон
    ema.get_updata(window_short=4, window_long=6, data_price=data_price)

    # Тестирование расчетов EMA с новыми параметрами окон
    print("\nПосле изменения параметров окон:")
    new_prices = [130, 132, 134, 135, 137, 138, 139, 140]
    list_short_2 = []
    list_long_2 = []
    for price in new_prices:
        signal = ema.calculator_ema(price)
        list_short_2.append(ema.previous_EMA_short)
        list_long_2.append(ema.previous_EMA_long)
        print(f"Цена: {price}, Сигнал: {signal}")
    print(f"\nИстория всех цен: {ema.data_price}")
    endtime = time.time()
    print(f"Время выполнения: {endtime-starttime}")

    # # Построение графика
    # plt.figure(figsize=(8, 6))  # Устанавливаем размер графика (необязательно)

    # plt.plot(range(len(data_price)), data_price, label='Список 1', marker='o')
    # plt.plot(range(len(list_short_2)), list_short_2, label='Список 2', marker='x')
    # plt.plot(range(len(list_long_2)), list_long_2, label='Список 3', marker='s')

    # # Добавление подписей к осям и заголовка
    # plt.xlabel('Индекс')
    # plt.ylabel('Значение')
    # plt.title('График трех списков')

    # # Добавление легенды
    # plt.legend()

    # # Включение сетки (необязательно)
    # plt.grid(True)

    # # Отображение графика
    # plt.show()

def main():
    # testSMA()
    testEMA()

if __name__ == "__main__":
    main()