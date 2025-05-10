#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Главный скрипт для построения QQ-plot на основе конфигурационного файла.
Запуск:
    python main.py
"""

import os.path

import yaml
from dotenv import load_dotenv
from loguru import logger

from data_loader import load_data
from distribution_fitter import get_distribution
from qq_plotter import qq_plot

load_dotenv()


def main() -> None:
    """Основной поток выполнения скрипта."""
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
        if data.empty:
            raise ValueError(
                "Нет данных для анализа после фильтрации пропусков."
            )

        # 3. Подбор распределения
        distribution = get_distribution(
            data=data,
            dist_type=config["distribution"]["type"],
        )
        logger.info(
            "Распределение {} успешно подобрано.".format(
                config['distribution']['type']
            )
        )

        # 4. Генерация и сохранение QQ-plot
        fig = qq_plot(
            data=data, dist=distribution, line=config["plot"]["show_line"]
        )
        save_folder = config["plot"]["output_dir"]
        save_filename = "QQ_{type}_{year}.{format}".format(
            type=config["distribution"]["type"],
            year=config["data"]["year"],
            format=config["plot"]["save_format"],
        )
        fig.savefig(os.path.join(save_folder, save_filename))
        logger.info("График успешно сохранен.")

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
