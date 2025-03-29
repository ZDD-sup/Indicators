class SEMA:
    """
    Класс SEMA (Smoothed Exponential Moving Average) предназначен для анализа финансовых данных
    с использованием экспоненциальной скользящей средней (EMA) и простой скользящей средней (SMA).

    Методы:
        - get_update_sema(window_short, window_long, data_price):  
          Инициализирует параметры и рассчитывает начальное значение EMA.
        
        - calculator_sema(price):  
          Добавляет новую цену в список, рассчитывает EMA и SMA, и определяет торговый сигнал.
        
    Вспомогательные методы:
        - _one_window_ema(price):  
          Рассчитывает EMA для последнего поступившего значения.
        
        - _one_window_sma():  
          Рассчитывает SMA для длинного периода.

    Использование:
        1. Создайте объект класса:  
            sema = SEMA()
        
        2. Установите параметры окна и передайте исторические данные:  
            sema.get_update_sema(window_short=10, window_long=50, data_price=[цены])
        
        3. Для каждой новой цены вызывайте метод calculator_sema(), чтобы получать торговый сигнал:  
            signal = sema.calculator_sema(новая_цена)
            print(signal)  # "Buy", "Sell" или "Neutral"
    """
    def __init__(self):
        """
        Инициализирует объект класса SEMA с начальными параметрами.
        """
        self.window_short = 0  # Длина короткого окна EMA
        self.window_long = 0   # Длина длинного окна SMA
        self.data_price = []   # Список исторических цен
        self.previous_EMA_short = None  # Предыдущее значение EMA
        self.K = 0  # Коэффициент сглаживания EMA
        self.previous_signal = None  # Последний торговый сигнал

    def get_update_sema(self, window_short: int, window_long: int, data_price: list):
        """
        Устанавливает параметры и рассчитывает начальное значение экспоненциальной средней (EMA).

        Args:
            window_short (int): Длина короткого окна для расчёта EMA.
            window_long (int): Длина длинного окна для расчёта SMA.
            data_price (list): Список исторических цен.

        Returns:
            None
        """
        self.window_short = window_short
        self.window_long = window_long
        self.data_price = data_price if data_price is not None else []
        self.K = 2 / (self.window_short + 1)

        if self.previous_EMA_short is None:
            len_data_price = len(self.data_price)
            if len_data_price < self.window_short:
                return None
            start_short = len_data_price - self.window_short
            self.previous_EMA_short = sum(self.data_price[start_short:]) / self.window_short

    def _one_window_ema(self, price: float):
        """
        Рассчитывает экспоненциальную скользящую среднюю (EMA) за один период.

        Если предыдущее значение EMA отсутствует, метод вернёт None.

        Args:
            price (float): Последняя поступившая цена.

        Returns:
            float | None: Новое значение EMA или None, если предыдущего значения нет.
        """
        if self.previous_EMA_short is None:
            return None

        ema_short = (price * self.K) + self.previous_EMA_short * (1 - self.K)
        self.previous_EMA_short = ema_short  # Обновляем предыдущее значение EMA

        return ema_short

    def _one_window_sma(self):
        """
        Рассчитывает простую скользящую среднюю (SMA) для длинного окна.

        Returns:
            float | None: Значение SMA, если данных достаточно, иначе None.
        """
        len_data_price = len(self.data_price)
        if len_data_price < self.window_long:
            return None

        start_long = len_data_price - self.window_long
        return sum(self.data_price[start_long:]) / self.window_long

    def calculator_sema(self, price: float):
        """
        Рассчитывает торговый сигнал на основе сравнений EMA и SMA.

        Args:
            price (float): Последняя поступившая цена.

        Returns:
            str: Один из возможных сигналов: "Buy", "Sell" или "Neutral".
        """
        self.data_price.append(price)  # Добавляем новую цену в список цен

        if len(self.data_price) > 1000:  # Ограничиваем количество хранимых цен
            self.data_price.pop(0)

        short_ema = self._one_window_ema(price)
        long_sma = self._one_window_sma()

        if short_ema is None or long_sma is None:
            return "Neutral"

        current_signal = "Neutral"
        if short_ema > long_sma:
            current_signal = "Buy"
        elif short_ema < long_sma:
            current_signal = "Sell"

        signal = "Neutral"
        if self.previous_signal is not None:
            if self.previous_signal == "Sell" and current_signal == "Buy":
                signal = "Buy"  # Пересечение снизу вверх
            elif self.previous_signal == "Buy" and current_signal == "Sell":
                signal = "Sell"  # Пересечение сверху вниз

        self.previous_signal = current_signal  # Обновляем предыдущий сигнал
        return signal
