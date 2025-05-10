"""
Модуль для подбора параметров распределений.
Поддерживает: normal, burr, gamma, demo (N(0,1)).
"""

from loguru import logger
from scipy import stats


def get_distribution(data, dist_type):
    """
    Возвращает распределение с параметрами.

    :param data: Данные для подбора (используется если fit_from_data=True)
    :param dist_type: Тип распределения (normal/burr/gamma/demo)
    """
    try:
        # Демо-режим: фиксированное нормальное распределение
        if dist_type == "demo":
            return stats.norm(loc=0, scale=1)

        # Выбор распределения
        dist = {
            "normal": stats.norm,
            "burr": stats.burr,
            "gamma": stats.gamma,
        }[dist_type]

        # Подбор или применение готовых параметров
        fit_params = dist.fit(data, floc=0)

        logger.info(f"Параметры {dist_type}: {fit_params}")
        return dist(*fit_params)

    except KeyError:
        raise ValueError(f"Неподдерживаемое распределение: {dist_type}")
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        raise
