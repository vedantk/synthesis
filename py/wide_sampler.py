import math
import struct
import random
from sampler import Sampler

class WideBandSampler(Sampler):
    def initialize(self):
        self.width = 16

    def pcm_to_repr(self, frame):
        val = struct.unpack('@i', frame)[0]
        return int(val / self.width)

    def repr_to_pcm(self, chunk):
        val = self.width * chunk 
        return struct.pack('@i', random.randint(0, self.width) + chunk)


