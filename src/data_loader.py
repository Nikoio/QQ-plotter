import os

import pandas as pd
import yaml
from loguru import logger

COLUMN_NAMES_FILE = "columns.yaml"


def get_column_names(folder_path):
    with open(
        os.path.join(folder_path, COLUMN_NAMES_FILE), "r", encoding="utf-8"
    ) as file:
        column_names = yaml.safe_load(file)["column_names"]
    return column_names


def load_data(folder_path, year, column, missing_values):
    """
    Читает данные из TXT файлов в папке, фильтруя по году.

    Параметры:
    - folder_path (str): Путь к папке с файлами.
    - year (str | int): "all" (все года) или конкретный год (например, 2003).

    Возвращает:
    - pd.DataFrame: DataFrame с данными и колонкой 'filename'.
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
