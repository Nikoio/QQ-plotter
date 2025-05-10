import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def qq_plot(data, dist=stats.norm, line=True, **plot_kwargs):

    # Конвертируем данные в numpy array
    sample = np.asarray(data)
    sample = sample[~np.isnan(sample)]  # Удаляем NaN

    # Сортируем данные
    sample_sorted = np.sort(sample)

    # Вычисляем теоретические квантили
    quantiles = dist.ppf(np.linspace(0.01, 0.99, len(sample)))

    # Создаем график
    fig, ax = plt.subplots(figsize=(6, 6))

    # Настраиваем аргументы по умолчанию для точек
    default_kwargs = {"marker": "o", "linestyle": "none", "alpha": 0.7}
    plot_kwargs = {**default_kwargs, **plot_kwargs}

    ax.plot(quantiles, sample_sorted, **plot_kwargs)

    # Добавляем линию сравнения
    if line:
        min_val = min(quantiles[0], sample_sorted[0])
        max_val = max(quantiles[-1], sample_sorted[-1])
        ax.plot([min_val, max_val], [min_val, max_val], "r--", alpha=0.5)

    ax.set_xlabel("Теоретические квантили")
    ax.set_ylabel("Эмпирические квантили")
    ax.set_title("QQ-plot")

    return fig


# Пример использования:
if __name__ == "__main__":
    # Генерируем случайные данные
    np.random.seed(42)
    normal_data = np.random.normal(loc=0, scale=1, size=100)

    # Создаем QQ-plot для нормального распределения
    qq_plot(normal_data, color="blue")

    plt.tight_layout()
    plt.show()
