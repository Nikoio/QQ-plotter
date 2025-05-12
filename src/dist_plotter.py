from typing import Optional
from venv import logger

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def dist_plot(
    data: np.ndarray,
    dist: stats.rv_continuous = stats.norm,
    limits: Optional[tuple[Optional[float], Optional[float]]] = None,
    title: str = "Distribution",
    figsize: tuple[int, int] = (12, 8),
    dpi: int = 100,
) -> plt.Figure:
    logger.info("Начало отрисовки графика распределения...")
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    ax.hist(
        data,
        bins=100,
        density=True,
        alpha=0.6,
        color="#02a01a",
        label="Histogram",
    )
    x = np.linspace(0, max(data), 1000)
    pdf_fitted = dist.pdf(x)
    ax.plot(x, pdf_fitted, color="#FF0000", label="Approximate distribution")

    ax.set_title(title)
    ax.set_xlabel("Scalar B, nT")
    ax.legend()
    ax.set_xlim(limits)

    return fig
