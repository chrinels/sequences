__all__ = ['LFSR']


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
