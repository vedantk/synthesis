import numpy
import struct
from sampler import Sampler, clamp

class DiffSampler(Sampler):
    def initialize(self):
        self.order = 2

    def pre_process(self):
        self.buf = numpy.diff(self.buf, self.order)
