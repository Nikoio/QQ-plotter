from scipy import stats


def get_distribution(data, dist_type):
    if dist_type == "demo":
        return stats.norm
    elif dist_type == "normal":
        dist = stats.norm
        params = dist.fit(data)
        fitted_dist = dist(*params)
        return fitted_dist
    elif dist_type == "burr":
        dist = stats.burr
        params = dist.fit(data)
        fitted_dist = dist(*params)
        return fitted_dist
    elif dist_type == "gamma":
        dist = stats.gamma
        params = dist.fit(data)
        fitted_dist = dist(*params)
        return fitted_dist
    else:
        raise Exception(f"Неизвестная функция {dist_type}")
