#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Главный модуль для построения QQ-графика на основе конфигурационного файла.

Основные функции:
- Загрузка и валидация конфигурации из YAML-файла.
- Обработка входных данных (фильтрация, загрузка из файлов).
- Подбор теоретического распределения.
- Генерация и сохранение графика.

Запуск:
    poetry run python -m src.main  # через Poetry
    или
    python src/main.py --config=config.yaml

Зависимости:
    - Конфигурационный файл (по умолчанию берется из переменных окружения).
    - Данные в папке ./data в формате YYYY.txt.

Обрабатываемые исключения:
    - FileNotFoundError: отсутствие конфига или данных.
    - ValueError: некорректные параметры конфига или пустые данные.
    - Общие исключения с логированием в qq_plot.log.

Пример использования:
    poetry run main
"""

import os.path

import numpy as np
import yaml
from dotenv import load_dotenv
from loguru import logger

from data_loader import load_data
from dist_plotter import dist_plot
from distribution_fitter import get_distribution
from qq_plotter import qq_plot

load_dotenv()


def main() -> None:
    """Основной поток выполнения скрипта.

    Шаги выполнения:
    1. Загрузка конфигурации из YAML-файла
        (путь через переменную окружения CONFIG_PATH).
    2. Валидация обязательных полей конфига.
    3. Загрузка данных из папки с фильтрацией по году и обработкой пропусков.
    4. Подбор параметров распределения (MLE или из конфига).
    5. Генерация QQ-графика с настройками из конфига.
    6. Сохранение результата в указанную папку.

    Исключения:
        Прерывает выполнение и логирует ошибки при:
        - Отсутствии конфига/данных
        - Некорректном формате года
        - Пустом датасете после фильтрации
        - Ошибках визуализации

    Логи:
        Все ключевые этапы и ошибки записываются через
        loguru в stdout.
    """
    logger.info("Начало работы...")
    config_path = os.getenv("CONFIG_PATH")
    try:
        # 1. Загрузка и валидация конфигурации
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        logger.info(f"Конфигурация загружена: {config['data']['column']}")

        # 2. Загрузка и предобработка данных
        data = load_data(
            folder_path=config["data"]["path"],
            column=config["data"]["column"],
            year=config["data"]["year"],
            missing_values=config["data"]["missing_values"],
        )
        if len(data) == 0:
            raise ValueError(
                "Нет данных для анализа после фильтрации пропусков."
            )
        data_size = len(data)
        logger.info(f"Данные загружены. Размер: {data_size}.")

        # 3. Подбор распределения
        distribution = get_distribution(
            data=data,
            year=config["data"]["year"],
            dist_type=config["distribution"]["type"],
            dist_params_dir=config["distribution"]["params_dir"]
        )
        logger.info(
            "Распределение {} успешно подобрано.".format(
                config["distribution"]["type"]
            )
        )

        # 4. Генерация и сохранение QQ-plot
        fig = qq_plot(
            data=data,
            dist=distribution,
            line=config["plot"]["show_line"],
            limits=config["plot"]["limits"],
        )
        save_folder = config["plot"]["output_dir"]
        save_filename = "{type}_{year}_QQ.{format}".format(
            type=config["distribution"]["type"],
            year=config["data"]["year"],
            format=config["plot"]["save_format"],
        )
        fig.savefig(os.path.join(save_folder, save_filename))
        logger.info("QQ-график успешно сохранен.")

        fig = dist_plot(
            data=data,
            dist=distribution,
            limits=config["plot"]["limits"],
        )
        save_filename = "{type}_{year}_dist.{format}".format(
            type=config["distribution"]["type"],
            year=config["data"]["year"],
            format=config["plot"]["save_format"],
        )
        fig.savefig(os.path.join(save_folder, save_filename))
        logger.info("График успешно сохранен.")

        # 5. Симуляция данных, генерация и сохранение QQ-plot
        logger.info("Начало симуляции данных")
        # Симуляция данных
        data = distribution.rvs(size=data_size)

        fig = qq_plot(
            data=data,
            dist=distribution,
            line=config["plot"]["show_line"],
            limits=config["plot"]["limits"],
        )
        save_folder = config["plot"]["output_dir"]
        save_filename = "{type}_{year}_QQ_sim.{format}".format(
            type=config["distribution"]["type"],
            year=config["data"]["year"],
            format=config["plot"]["save_format"],
        )
        fig.savefig(os.path.join(save_folder, save_filename))
        logger.info("QQ-график симуляции успешно сохранен.")

        # Фильтрация данных, которые попадут на график
        fig = dist_plot(
            data=data,
            dist=distribution,
            limits=config["plot"]["limits"],
        )
        save_filename = "{type}_{year}_dist_sim.{format}".format(
            type=config["distribution"]["type"],
            year=config["data"]["year"],
            format=config["plot"]["save_format"],
        )
        fig.savefig(os.path.join(save_folder, save_filename))
        logger.info("График симуляции успешно сохранен.")

    except FileNotFoundError as e:
        logger.error(f"Ошибка: {e}")
        raise e
    except ValueError as e:
        logger.error(f"Ошибка в данных: {e}")
        raise e
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}", exc_info=True)
        raise e


if __name__ == "__main__":
    main()
