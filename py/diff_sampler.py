import numpy
import struct
from sampler import Sampler, clamp

class DiffSampler(Sampler):
    def pre_process(self):
        print "Pre-processing data..."
        tmp = [struct.unpack('@i', frame)[0]
               for frame in self.buf]
        self.buf = numpy.diff(tmp)

    def repr_to_pcm(self, chunk):
        return struct.pack('@i', clamp(chunk, -2147483647, 2147483647))
