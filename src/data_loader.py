"""
Модуль для загрузки и предобработки данных из текстовых файлов.

Основные функции:
- Чтение метаданных о колонках из YAML-файла.
- Фильтрация и загрузка данных из файлов формата YYYY.txt.
- Обработка пропущенных значений.

Пример использования:
    from data_loader import load_data
    df = load_data(
        folder_path="./data",
        year=2005,
        column="Scalar B, nT",
        missing_values=[9999.99, 99999.9]
    )
"""

import os

import pandas as pd
import yaml
from loguru import logger

COLUMN_NAMES_FILE = "columns.yaml"


def get_column_names(folder_path: str) -> list[str]:
    """Получает названия колонок из YAML-файла.

    Args:
        folder_path: Путь к папке с файлом columns.yaml.

    Returns:
        Список названий колонок в порядке их следования в данных.

    Raises:
        FileNotFoundError: Если файл columns.yaml не найден.
        yaml.YAMLError: При ошибке парсинга YAML.

    Пример:
        get_column_names("./data")
        ['Year', 'Day', 'Hour', ..., 'Vz Velocity, km/s, GSE']
    """
    with open(
        os.path.join(folder_path, COLUMN_NAMES_FILE), "r", encoding="utf-8"
    ) as file:
        column_names = yaml.safe_load(file)["column_names"]
    return column_names


def load_data(
    folder_path: str, year: str | int, column: str, missing_values: list[float]
) -> pd.DataFrame:
    """Загружает и фильтрует данные из текстовых файлов.

    Args:
        folder_path: Путь к папке с файлами данных (формат: YYYY.txt).
        year: Год для фильтрации ("all" - все года).
        column: Название колонки для извлечения.
        missing_values: Список значений, интерпретируемых как пропуски.

    Returns:
        DataFrame с данными указанной колонки (без пропусков).

    Raises:
        ValueError: При ошибках:
            - Некорректный путь к папке
            - Отсутствие подходящих файлов
            - Пустой результат после фильтрации

    Особенности:
        - Игнорирует файлы не в формате "YYYY.txt"
        - Автоматически определяет разделители (sep="\\s+")
        - Объединяет данные из всех подходящих файлов
        - Удаляет строки с NaN после обработки missing_values

    Пример:
        Загрузка всех данных за 2005 год:
        load_data("./data", 2005, "Scalar B, nT", [9999.99])
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"Папка '{folder_path}' не существует.")

    dfs = []

    for filename in os.listdir(folder_path):
        if not filename.endswith(".txt"):
            continue

        # Проверяем, соответствует ли имя файла шаблону "YYYY.txt"
        file_year = filename.split(".")[0]  # Убираем .txt
        if not file_year.isdigit() or len(file_year) != 4:
            continue  # Пропускаем файлы не в формате "YYYY.txt"

        # Если указан конкретный год — пропускаем неподходящие
        if year == "all" or str(file_year) == str(year):
            # Читаем файл
            logger.info(f"Загружаю данные из файла {filename}...")
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(
                file_path,
                sep="\\s+",
                names=get_column_names(folder_path),
                usecols=[column],
                na_values=missing_values,
            ).dropna()

            dfs.append(df)
    data = pd.concat(dfs, ignore_index=True)
    return data
