import datetime as dt


def variant_time():
    """
    Генерация вариантов времени для заказов.

    Эта функция генерирует список вариантов времени для заказов, начиная с текущего времени
    плюс 40 минут и с шагом в 20 минут между каждым вариантом. Всего генерируется 13 вариантов времени.
    Время представляется в формате "чч:мм".

    Returns
    -------
    list of str
        Список вариантов времени для заказов в формате "чч:мм".

    Notes
    -----
    - Время генерируется на основе текущего времени и может меняться при каждом вызове функции.
    - Функция использует локальное время устройства, на котором она выполняется.

    """
    min_order_time = dt.datetime.now() + dt.timedelta(minutes=40)

    min_hour = str(min_order_time.hour)
    min_hour = "0" * (2 - len(min_hour)) + min_hour
    min_minute = str(min_order_time.minute)
    min_minute = "0" * (2 - len(min_minute)) + min_minute

    time_range = ["%s:%s" % (min_hour, min_minute)]
    next_order_time = min_order_time
    for i in range(12):
        next_order_time = next_order_time + dt.timedelta(minutes=20)
        next_hour = str(next_order_time.hour)
        next_hour = "0" * (2 - len(next_hour)) + next_hour
        next_minute = str(next_order_time.minute)
        next_minute = "0" * (2 - len(next_minute)) + next_minute
        time_range.append("%s:%s" % (next_hour, next_minute))
    return time_range


def time_of_order():
    """
    Получение текущей даты и времени заказа.

    Эта функция возвращает текущую дату и время в формате "дд.мм.гггг" и "чч:мм" соответственно.

    Returns
    -------
    tuple of str
         Кортеж, содержащий текущую дату и время в формате "дд.мм.гггг" и "чч:мм" соответственно.

    Notes
    -----
    - Дата и время генерируются на основе текущего момента времени и могут меняться при каждом вызове функции.
    - Функция использует локальное время устройства, на котором она выполняется.

    """
    order_date = dt.datetime.now().strftime('%d.%m.%Y')
    order_time = dt.datetime.now().strftime('%H:%M')
    return order_date, order_time
