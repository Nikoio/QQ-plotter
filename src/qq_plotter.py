"""
Модуль для построения QQ-графиков с расширенными возможностями настройки.
"""

from pathlib import Path
from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def qq_plot(
    data: np.ndarray,
    dist: stats.rv_continuous = stats.norm,
    line: bool = True,
    limits: Optional[tuple[Optional[float], Optional[float]]] = None,
    title: str = "QQ-Plot",
    marker_color: str = "blue",
    line_color: str = "red",
    grid: bool = True,
    figsize: tuple[int, int] = (8, 8),
    dpi: int = 100,
    save_path: Optional[Union[str, Path]] = None,
    **plot_kwargs,
) -> plt.Figure:
    """
    Строит и сохраняет QQ-график для сравнения выборки
    с теоретическим распределением.

    Parameters:
        data : Массив данных для анализа
        dist : Распределение из scipy.stats (по умолчанию нормальное)
        line : Отображать линию y=x
        limits: Границы осей в формате (min, max). Примеры:
            (-5, 5)    # Фиксированные границы
            (None, 3)  # Автоматический минимум, максимум=3
        title : Заголовок графика
        marker_color : Цвет точек
        line_color : Цвет линии
        grid : Отображать сетку
        figsize : Размер фигуры (ширина, высота)
        dpi : Разрешение изображения
        save_path : Путь для сохранения графика (None - не сохранять)
        **plot_kwargs : Дополнительные параметры для plt.plot()

    Returns:
        plt.Figure: Объект фигуры matplotlib

    Raises:
        ValueError: Если данные пусты после очистки

    Пример:
        data = np.random.normal(size=100)
        qq_plot(data, title="Normal Distribution", save_path="plot.png")
    """
    # Конвертация и очистка данных
    sample = np.asarray(data)
    sample = sample[np.isfinite(sample)]  # Удаляем NaN и Inf

    if len(sample) == 0:
        raise ValueError("Нет данных для построения графика после очистки")

    # Расчет квантилей
    sample_sorted = np.sort(sample)
    quantiles = dist.ppf(np.linspace(0.01, 0.99, len(sample)))

    # Создание фигуры
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Построение точек
    ax.plot(
        quantiles,
        sample_sorted,
        marker="o",
        linestyle="none",
        color=marker_color,
        alpha=0.2,
        markersize=6,
        **plot_kwargs,
    )

    # Установка пределов осей
    if limits is not None:
        ax.set_ylim(*limits)
        ax.set_xlim(ax.get_ylim())

    # Построение линии y=x
    if line:
        min_val = min(np.nanmin(quantiles), np.nanmin(sample_sorted))
        max_val = max(np.nanmax(quantiles), np.nanmax(sample_sorted))
        ax.plot(
            [min_val, max_val],
            [min_val, max_val],
            color=line_color,
            linestyle="--",
            linewidth=1.5,
        )

        # Линия среднего
        mean_point = data.mean()
        print(mean_point)
        ax.axhline(y=mean_point, color="blue", alpha=0.5)

    # Настройка оформления
    ax.set_title(title, fontsize=14, pad=20)
    ax.set_xlabel("Теоретические значения", fontsize=12)
    ax.set_ylabel("Эмпирические значения", fontsize=12)

    if grid:
        ax.grid(True, alpha=0.3, linestyle="--")

    plt.tight_layout()

    # Сохранение графика
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")

    return fig
