import math
import struct
from sampler import Sampler

class WideBandSampler(Sampler):
    def initialize(self):
        self.width = 16

    def pre_process(self):
        self.buf = [int(val / self.width) for val in self.buf]

    def repr_to_pcm(self, chunk):
        val = self.width * chunk 
        return super(WideBandSampler, self).repr_to_pcm(val)

