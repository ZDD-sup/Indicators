class SMA:
    """
    Класс для расчета скользящих средних (SMA) и генерации сигналов
    покупки/продажи на основе пересечения краткосрочной и долгосрочной SMA.
    """
    def __init__(self):
        """
        Инициализирует объект SMA с начальными значениями.

        Аргументы:
            None
        """
        self.window_short = None  # Длина окна для краткосрочной SMA
        self.window_long = None   # Длина окна для долгосрочной SMA
        self.data_price = []      # Список исторических цен
        self.previous_signal = None  # Для хранения предыдущего торгового сигнала

    def get_updata(self, window_short: int, window_long: int, data_price: list):
        """
        Устанавливает параметры SMA (короткий и длинный окна) и инициализирует исторические данные цен.

        Этот метод должен быть вызван один раз в начале работы или при необходимости обновить параметры.

        Аргументы:
            window_short (int): Размер окна для краткосрочной скользящей средней.
            window_long (int): Размер окна для долгосрочной скользящей средней.
            data_price (list): Список исторических цен.

        Возвращаемое значение:
            None
        """
        self.window_short = window_short
        self.window_long = window_long
        self.data_price = data_price if data_price is not None else []

    def calculate_sma(self, price: float):
        """
        Добавляет новую цену в список цен и рассчитывает сигналы покупки или продажи на основе пересечения 
        краткосрочной и долгосрочной скользящих средних.

        Если краткосрочная SMA пересекает долгосрочную снизу вверх, генерируется сигнал на покупку.
        Если краткосрочная SMA пересекает долгосрочную сверху вниз, генерируется сигнал на продажу.

        Аргументы:
            price (float): Новая цена, поступающая для анализа.

        Возвращаемое значение:
            str: Сигнал "Buy", "Sell" или "Neutral".
                 "Buy" — если краткосрочная SMA пересекает долгосрочную снизу вверх.
                 "Sell" — если краткосрочная SMA пересекает долгосрочную сверху вниз.
                 "Neutral" — если пересечения не произошло или недостаточно данных для расчета SMA.
        """
        self.data_price.append(price)  # Добавляем новое значение в список цен

        len_data_price = len(self.data_price)
        if len_data_price > 1000:
            self.data_price.pop(0)  # Удаляем старые данные, если их слишком много

        if len(self.data_price) < self.window_long:
            return None  # Недостаточно данных для расчета SMA

        # Рассчитываем значения для короткой SMA
        start_short = max(0, len(self.data_price) - self.window_short)
        short_sma = sum(self.data_price[start_short:len_data_price]) / self.window_short

        # Рассчитываем значения для долгосрочной SMA
        start_long = max(0, len(self.data_price) - self.window_long)
        long_sma = sum(self.data_price[start_long:len_data_price]) / self.window_long

        # Логика определения текущего сигнала
        current_signal = "Neutral"
        if short_sma > long_sma:
            current_signal = "Buy"
        elif short_sma < long_sma:
            current_signal = "Sell"

        # Определяем момент пересечения
        signal = "Neutral"
        if self.previous_signal is not None:
            if self.previous_signal == "Sell" and current_signal == "Buy":
                signal = "Buy"  # Пересечение снизу вверх
            elif self.previous_signal == "Buy" and current_signal == "Sell":
                signal = "Sell"  # Пересечение сверху вниз

        self.previous_signal = current_signal  # Обновляем предыдущий сигнал
        return signal
