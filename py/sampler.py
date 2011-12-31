#!/usr/bin/pypy

import sys
import wave
import math
import struct
import random
from markov import MarkovChain

class Sampler:
    def __init__(self, fname, nr_secs=15):
        '''Load <nr_secs> of PCM data from <fname>.'''
        self.initialize()
        self.fname = fname
        f = wave.open(self.fname, 'r')
        self.params = f.getparams()
        nr_frames = nr_secs * f.getframerate()
        frames = f.readframes(nr_frames)
        self.buf = [self.pcm_to_repr(frames[i:i+4])
                    for i in xrange(0, nr_frames * 4, 4)]

    def initialize(self):
        pass

    def pcm_to_repr(self, frame):
        '''Convert 4 bytes of PCM data into any format.'''
        return frame

    def repr_to_pcm(self, chunk):
        '''Convert chunk into a 4 byte PCM frame.'''
        return chunk

    def sample(self, outf, nr_frames=1e6, n=3):
        '''Sample using an n-gram into the given file.'''
        chain = MarkovChain(n)
        chain.add_sequence(self.buf)
        gen = chain.walk()
        out = wave.open(outf, 'wb')
        out.setparams(self.params)
        out.setnframes(nr_frames)
        chunk = nr_frames / 100
        for k in xrange(nr_frames):
            if k % chunk == 0:
                print k / chunk, "%"
            out.writeframes(self.repr_to_pcm(next(gen)))

class WideBandSampler(Sampler):
    def initialize(self):
        self.width = 16

    def pcm_to_repr(self, frame):
        val = struct.unpack('@i', frame)[0]
        return int(val / self.width)

    def repr_to_pcm(self, chunk):
        val = self.width * chunk 
        return struct.pack('@i', random.randint(0, self.width) + chunk)

if __name__ == '__main__':
    print "Loading data..."
    gen = WideBandSampler(sys.argv[1])
    print "Sampling chain..."
    gen.sample('bsp-out.wav')
