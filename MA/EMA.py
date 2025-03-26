class EMA:
    """
    Класс для расчета экспоненциальных скользящих средних (EMA) и генерации торговых сигналов на их основе.

    Использует две EMA с разными периодами (короткий и длинный) для определения моментов
    пересечения, которые могут служить сигналами на покупку или продажу.
    """
    def __init__(self):
        """
        Инициализирует объект EMA с начальными значениями.
        """
        self.window_short = None  # Длина короткого периода EMA
        self.K_short = None     # Сглаживающий коэффициент для короткого периода EMA
        self.window_long = None   # Длина длинного периода EMA
        self.K_long = None      # Сглаживающий коэффициент для длинного периода EMA
        self.data_price = []# Список для хранения ценовых данных

        # Инициализация прошлых значений EMA
        self.previous_EMA_short = None  # Предыдущее значение короткой EMA
        self.previous_EMA_long = None   # Предыдущее значение длинной EMA
        self.prev_signal = "Neutral"    # Последний торговый сигнал (по умолчанию "Нейтральный")

    def get_updata(self, window_short: int, window_long: int, data_price: list):
        """
        Устанавливает значения периодов EMA и инициализирует начальные значения EMA на основе предоставленных исторических данных.

        Вызывать эту функцию следует один раз в начале работы или при необходимости обновить параметры EMA и начальные значения.

        Args:
            window_short (int): Длина короткого периода EMA.
            window_long (int): Длина длинного периода EMA.
            data_price (list): Список исторических ценовых данных.
        """
        self.window_short = window_short  # Устанавливаем длину короткого периода EMA
        self.window_long = window_long    # Устанавливаем длину длинного периода EMA
        self.data_price = data_price if data_price is not None else []# Присваиваем список цен, если он не None, иначе создаем пустой список

        len_data_price = len(self.data_price) # Получаем длину списка цен
        start_short = max(0, len(self.data_price) - self.window_short) # Определяем начальный индекс для расчета начальной короткой EMA
        self.previous_EMA_short = sum(self.data_price[start_short:len_data_price]) / self.window_short # Рассчитываем начальное значение короткой EMA как среднее значение за короткий период

        start_long = max(0, len(self.data_price) - self.window_long) # Определяем начальный индекс для расчета начальной длинной EMA
        self.previous_EMA_long = sum(self.data_price[start_long:len_data_price]) / self.window_long # Рассчитываем начальное значение длинной EMA как среднее значение за длинный период

        self.K_short = 2 / (self.window_short + 1) # Рассчитываем сглаживающий коэффициент для короткой EMA
        self.K_long = 2 / (self.window_long + 1)  # Рассчитываем сглаживающий коэффициент для длинной EMA

    def calculator_ema(self, price: float):
        """
        Рассчитывает значения короткой и длинной EMA для новой цены и генерирует торговый сигнал.

        Вызывать эту функцию следует для каждой новой поступающей цены.

        Args:
            price (float): Новая ценовая точка.

        Returns:
            str: Торговый сигнал ("Buy", "Sell" или "Neutral").
        """
        self.data_price.append(price) # Добавляем новое значение в список цен

        len_data_price = len(self.data_price) # Получаем длину списка цен
        if len_data_price > 1000: # Если количество данных превышает 1000
            self.data_price.pop(0) # Удаляем самый старый элемент из списка цен, чтобы поддерживать его размер

        ema_short = (price * self.K_short) + self.previous_EMA_short * (1 - self.K_short) # Рассчитываем значение короткой EMA по формуле
        ema_long = (price * self.K_long) + self.previous_EMA_long * (1 - self.K_long)   # Рассчитываем значение длинной EMA по формуле

        if ema_short is None or ema_long is None: # Если какое-либо значение EMA не рассчитано (например, при недостатке данных)
            return "Neutral"  # Возвращаем "Нейтральный" сигнал

        if ema_short > ema_long and self.prev_signal != "Buy": # Если короткая EMA пересекает длинную EMA снизу вверх и предыдущий сигнал не был "Покупка"
            self.prev_signal = "Buy" # Устанавливаем текущий сигнал как "Покупка"
            return "Buy"  # Возвращаем сигнал на покупку
        elif ema_short < ema_long and self.prev_signal != "Sell": # Если короткая EMA пересекает длинную EMA сверху вниз и предыдущий сигнал не был "Продажа"
            self.prev_signal = "Sell" # Устанавливаем текущий сигнал как "Продажа"
            return "Sell" # Возвращаем сигнал на продажу
        else: # В остальных случаях (нет пересечения или сигнал не изменился)
            self.prev_signal = "Neutral" # Устанавливаем текущий сигнал как "Нейтральный"

        self.previous_EMA_short = ema_short # Обновляем предыдущее значение короткой EMA
        self.previous_EMA_long = ema_long   # Обновляем предыдущее значение длинной EMA

        return self.prev_signal # Возвращаем текущий торговый сигнал