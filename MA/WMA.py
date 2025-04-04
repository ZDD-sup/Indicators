class WMA:
    """
    Класс WMA (Weighted Moving Average) реализует стратегию торговли на основе взвешенных скользящих средних.

    Атрибуты:
        window_short (int): Размер короткого окна WMA.
        window_long (int): Размер длинного окна WMA.
        data_price (list): Список исторических цен.
        previous_signal (str | None): Предыдущий торговый сигнал ("Buy", "Sell" или "Neutral").

    Методы:
        startWMA(short, long, data_price):
            Инициализирует параметры окон и начальный список цен.
        
        one_window_wma(win_size, price, data_price):
            Вычисляет взвешенную скользящую среднюю для одного окна.

        calculator_wma(price):
            Рассчитывает короткую и длинную WMA, генерирует торговый сигнал при их пересечении.
    """

    def __init__(self):
        self.window_short = None
        self.window_long = None
        self.data_price = []
        self.previous_signal = None

    def startWMA(self, short: int, long: int, data_price: list):
        """
        Устанавливает параметры для расчёта WMA и начальные данные.

        Аргументы:
            short (int): Размер короткого окна.
            long (int): Размер длинного окна.
            data_price (list): Исторические цены.
        """
        self.window_short = short
        self.window_long = long
        self.data_price = data_price if data_price is not None else []

    def one_window_wma(self, win_size: int, price: float, data_price: list):
        """
        Рассчитывает взвешенную скользящую среднюю (WMA) для одного окна.

        Аргументы:
            win_size (int): Размер окна для WMA.
            price (float): Новая поступившая цена (добавляется в конец data_price).
            data_price (list): Исторические цены.

        Возвращает:
            float | None: Значение WMA, если достаточно данных, иначе None.
        """
        # Добавляем новую цену в конец списка
        data_price.append(price)

        # Удаляем старые данные, если список становится слишком длинным
        if len(data_price) > 1000:
            data_price.pop(0)

        # Если данных меньше, чем нужно — WMA не вычисляется
        if len(data_price) < win_size:
            return None

        # Извлекаем последние win_size значений
        recent_prices = data_price[-win_size:]
        
        # Формируем список весов от 1 до win_size
        weights = list(range(1, win_size + 1))

        # Взвешенная сумма: цена * вес
        weighted_sum = sum(p * w for p, w in zip(recent_prices, weights))
        weight_total = sum(weights)

        # Делим взвешенную сумму на сумму весов
        wma = weighted_sum / weight_total
        return wma

    def calculator_wma(self, price: float):
        """
        Основной метод: добавляет новую цену, рассчитывает короткую и длинную WMA,
        сравнивает их и генерирует торговый сигнал.

        Аргументы:
            price (float): Текущая цена актива.

        Возвращает:
            str: Сигнал ("Buy", "Sell" или "Neutral").
        """
        # Если недостаточно данных для длинной WMA — сигнал не рассчитываем
        if len(self.data_price) < self.window_long:
            return "Neutral"
        
        # Добавляем новую цену
        self.data_price.append(price)

        # Расчёт короткой WMA
        weighted_sum = sum(p * w for p, w in zip(
            self.data_price[-self.window_short:], 
            list(range(1, self.window_short + 1))
        ))
        weight_total = sum(range(1, self.window_short + 1))
        short_wma = weighted_sum / weight_total

        # Расчёт длинной WMA
        weighted_sum = sum(p * w for p, w in zip(
            self.data_price[-self.window_long:], 
            list(range(1, self.window_long + 1))
        ))
        weight_total = sum(range(1, self.window_long + 1))
        long_wma = weighted_sum / weight_total

        # Если по какой-то причине не удалось посчитать — выход
        if short_wma is None or long_wma is None:
            return "Neutral"

        # Определяем текущий сигнал на основе сравнения WMA
        current_signal = "Neutral"
        if short_wma > long_wma:
            current_signal = "Buy"
        elif short_wma < long_wma:
            current_signal = "Sell"

        # Проверяем на пересечение сигналов
        signal = "Neutral"
        if self.previous_signal:
            if self.previous_signal == "Sell" and current_signal == "Buy":
                signal = "Buy"
            elif self.previous_signal == "Buy" and current_signal == "Sell":
                signal = "Sell"

        # Обновляем предыдущее состояние сигнала
        self.previous_signal = current_signal
        return signal
