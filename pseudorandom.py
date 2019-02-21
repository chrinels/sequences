#!/usr/bin/env python3

import numpy as np
from math import gcd

class LFSR:

    def __init__(self, taps, init_register, output=None, samples_per_frame=None, matlab=False):
        if taps[-1] != 0:
            raise AttributeError("The first and last taps must be connected.")
        if taps[0] != len(init_register):
            raise AttributeError("The first and last taps must be connected.")
        if output is None:
            output = [len(init_register)]
        if any([((i > len(init_register)) | (i < 1)) for i in output]):
            raise AttributeError("The output tap(s) must exist!")

        if samples_per_frame is None:
            self.samples = 2**len(init_register) - 1
        else:
            self.samples = samples_per_frame

        self.init_register = init_register.copy()
        self.register = init_register.copy()
        self.output = output
        if matlab:
            self.taps = [taps[0] - tap for tap in reversed(taps)]
            self.taps = self.taps[:-1]
        else:
            self.taps = taps[:-1]
        self.cycled_through = False

    def reset(self):
        self.register = self.init_register.copy()

    def step(self):
        frame = []
        for _ in range(self.samples):
            frame.append(self.shift())
        return frame

    def shift(self):
        out = [self.register[i-1] for i in self.output]
        if len(out) > 1:
            out = sum(out) % 2
        else:
            out = out[0]

        feedback = sum([self.register[i-1] for i in self.taps]) % 2
        for i in reversed(range(len(self.register) - 1)):
            self.register[i+1] = self.register[i]

        self.register[0] = feedback
        if self.register == self.init_register:
            self.cycled_through = True
        return out


class GoldSequence:

    def __init__(self, first_polynomial, first_initial_conditions,
                 second_polynomial, second_initial_conditions,
                 samples_per_frame=None, index=0, matlab=False, debug=False):
        self.mls1 = LFSR(first_polynomial, first_initial_conditions, samples_per_frame=samples_per_frame, matlab=matlab)
        self.mls2 = LFSR(second_polynomial, second_initial_conditions, samples_per_frame=samples_per_frame, matlab=matlab)
        self.index = index
        self.cycled_through = False
        self.debug = debug

    def step(self):
        u = self.mls1.step()
        v = np.roll(self.mls2.step(), -self.index).tolist()
        g = (np.logical_xor(u, v) * 1).tolist()
        if self.debug:
            print("u = {}\nv = {}\nG = {}".format(u, v, g))
        if self.mls1.cycled_through or self.mls2.cycled_through:
            self.cycled_through = True
        return g

    def reset(self):
        self.mls1.reset()
        self.mls2.reset()


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

        if gcd(self.n_zc, self.u) is not 1:
            raise ValueError("gcd(n_zc, u) is not 1. u and n_zc most be coprime.")

    def generate(self):
        n = np.array(range(self.n_zc))
        return np.exp( -1j*np.pi*self.u*n*(n + self.cf + 2*self.q) / self.n_zc )


def write_seq_to_file(filename, seq, dt='complex'):
    seq = np.array(seq, dtype=dt)
    try:
        fid = open(filename, mode="wt", encoding="utf-8", newline="\n")
        for i in seq:
            fid.write("{},{}\n".format(np.real(i), np.imag(i)))
        fid.close()
    except OSError as er:
        print(er)
        pass


if __name__ == "__main__":

    # Gold sequence
    init = [0, 0, 0, 0, 0, 0, 0, 1]

    poly1 = [8, 6, 5, 3, 0]
    poly2 = [8, 6, 5, 2, 0]
    frame_length = 2**len(init) - 1     # Maximum length before the code repeats itself.

    gold = GoldSequence(poly1, init, poly2, init,
                        samples_per_frame=frame_length, index=0, matlab=True, debug=False)
    gold_sequence = (2 * np.array(gold.step()) - 1)

    # Zadoff-Chu waveform
    zc = ZadoffChu(1353, 7, 1)
    chu = zc.generate()

    # Write sequences to file(s)
    write_seq_to_file("goldseq.txt", gold_sequence, dt='int16')     # int16 is for the FMCOMMS3-board.
    write_seq_to_file("chu.txt", chu, dt='complex')
