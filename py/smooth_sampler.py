import struct
from sampler import Sampler

class SmoothSampler(Sampler):
    def pre_process(self):
        for i in xrange(1, len(self.buf) - 1):
            self.buf[i] = int(sum(self.buf[i-1:i+2]) / 3)
