"""精度计算模块。

提供泛函计算中的数值精度分析与自适应精度控制。
"""

import jax.numpy as jnp


def relative_error(approx, exact):
    """计算相对误差。

    Args:
        approx: 近似值
        exact: 精确值

    Returns:
        float: 相对误差
    """
    return jnp.abs(approx - exact) / (jnp.abs(exact) + 1e-12)


def convergence_rate(errors):
    """估计收敛阶。

    Args:
        errors: 各步误差序列

    Returns:
        float: 估计的收敛阶
    """
    if len(errors) < 3:
        return 0.0
    rates = jnp.log(errors[2:] / errors[1:-1]) / jnp.log(errors[1:-1] / errors[:-2])
    return float(jnp.nanmean(rates))