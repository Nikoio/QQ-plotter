"""
Модуль для подбора параметров распределений.
Поддерживает: normal, burr, gamma, demo (N(0,1)).
"""
import os

from loguru import logger
from scipy import stats
import yaml


def get_distribution(data, year, dist_type, dist_params_dir):
    """
    Возвращает распределение с параметрами.

    :param data: Данные для подбора (используется если fit_from_data=True)
    :param year: Год выборки (для файла параметров)
    :param dist_type: Тип распределения (normal/burr/gamma/demo)
    :param dist_params_dir: Путь, куда сохранять и  откуда загружать параметры аппроксимации
    """
    logger.info("Начало подбора распределения...")
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
        params_path = os.path.join(dist_params_dir, f"{dist_type}_{year}_params.yaml")
        if os.path.exists(params_path):
            logger.info(f"Загружаю параметры распределения из файла {params_path}")
            with open(params_path, "r", encoding="utf-8") as file:
                fit_params = yaml.safe_load(file)
        else:
            fit_params = dist.fit(data, floc=0)
            with open(params_path, "w") as outfile:
                yaml.dump([float(p) for p in fit_params], outfile)

        logger.info(f"Параметры {dist_type}: {fit_params}")
        return dist(*fit_params)

    except KeyError:
        raise ValueError(f"Неподдерживаемое распределение: {dist_type}")
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        raise
