from math import gcd
import numpy as np

__all__ = ["ZadoffChu"]


class ZadoffChu:

    def __init__(self, n_zc, u, q=0):
        self.n_zc = n_zc
        self.u = u
        self._check_parameter_requirements()

        self.cf = n_zc % 2
        self.q = q

    def _check_parameter_requirements(self):
        if (self.u < 0) or (self.u > self.n_zc):
            raise ValueError('"u" must lie in the range: 0 < u < n_zc')

        if gcd(self.n_zc, self.u) != 1:
            raise ValueError("gcd(n_zc, u) is not 1. u and n_zc most be coprime.")

    def generate(self):
        n = np.array(range(self.n_zc))
        return np.exp(-1j*np.pi*self.u*n*(n + self.cf + 2*self.q) / self.n_zc)


if __name__ == "__main__":
    zc = ZadoffChu(1353, 7, 1)
    print(zc.generate())
