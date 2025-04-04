class RSI:
    """
    Класс для расчета индикатора Relative Strength Index (RSI).
    """

    def __init__(self):
        """
        Инициализация пустого экземпляра RSI. Все параметры передаются через initialize_rsi().
        """
        self.period = None
        self.data_price = []
        self.avg_gain = None
        self.avg_loss = None
        self.previous_rsi = None

    def initialize_rsi(self, period: int, data_price: list[float]):
        """
        Инициализация параметров RSI. Вызывается один раз перед использованием.

        Аргументы:
            period (int): Период RSI (чаще всего 14).
            data_price (list[float]): Исторические цены (должно быть не менее period + 1 значений).
        """
        if len(data_price) <= period:
            raise ValueError("Для инициализации RSI необходимо минимум period + 1 значений цен.")

        self.period = period
        self.data_price = data_price[:]

        # Расчёт первичных приростов и потерь
        gains = [max(data_price[i] - data_price[i - 1], 0) for i in range(1, period + 1)]
        losses = [abs(min(data_price[i] - data_price[i - 1], 0)) for i in range(1, period + 1)]

        self.avg_gain = sum(gains) / period
        self.avg_loss = sum(losses) / period

        # Вычисляем начальное значение RSI
        if self.avg_loss == 0:
            self.previous_rsi = 100.0
        else:
            rs = self.avg_gain / self.avg_loss
            self.previous_rsi = 100 - (100 / (1 + rs))

    def update_price(self, price: float) -> float | None:
        """
        Обновляет список цен и рассчитывает новое значение RSI.

        Аргументы:
            price (float): Новое значение цены.

        Возвращает:
            float | None: RSI, если достаточно данных, иначе None.
        """
        if self.period is None or not self.data_price:
            raise RuntimeError("RSI не инициализирован. Сначала вызовите initialize_rsi().")

        self.data_price.append(price)
        if len(self.data_price) > 1000:
            self.data_price.pop(0)

        delta = self.data_price[-1] - self.data_price[-2]
        gain = max(delta, 0)
        loss = abs(min(delta, 0))

        # Обновление средних по методу Уайлдера
        self.avg_gain = (self.avg_gain * (self.period - 1) + gain) / self.period
        self.avg_loss = (self.avg_loss * (self.period - 1) + loss) / self.period

        if self.avg_loss == 0:
            rsi = 100.0
        else:
            rs = self.avg_gain / self.avg_loss
            rsi = 100 - (100 / (1 + rs))

        self.previous_rsi = rsi
        return rsi
