def vdf_compute(x: int, T: int, N: int) -> int:
    """模平方链，计算 y = x^{2^T} mod N"""
    y = x
    for _ in range(T):
        y = pow(y, 2, N)
    return y

def vdf_verify(y: int, x: int, T: int, N: int) -> bool:
    """验证 y 是否为 x^{2^T} mod N"""
    z = x
    for _ in range(T):
        z = pow(z, 2, N)
    return z == y
