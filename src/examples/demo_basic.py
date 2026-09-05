# demo_basic.py
import jax.numpy as jnp
from jax import grad, hessian

# 公理 I：定义"存在"就是一个泛函
def existence_functional(psi, gamma):
    # 一个最简单的泛函：类似于自由能/作用量
    return 0.5 * gamma * jnp.sum(psi**2)

# 公理 II & III：计算演化方向与精度
def analyze_entity(state, gamma=1.0):
    F = lambda s: existence_functional(s, gamma)
    
    # 梯度（决定演化方向，对应"力"或"预测误差"）
    gradient = grad(F)(state)
    
    # 精度（Hessian矩阵的二阶迹，对应"质量"或"注意力曲率"）
    hessian_matrix = hessian(F)(state)
    precision_metric = jnp.trace(hessian_matrix) 
    
    return {
        "free_energy": F(state),
        "force": -gradient,        # 负梯度（物理上指向低能方向）
        "precision": precision_metric
    }

# 测试：初始状态为 [1.0, -0.5]
result = analyze_entity(jnp.array([1.0, -0.5]), gamma=2.0)
print("泛函一元论核心计算结果:", result)