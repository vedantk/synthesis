#!/usr/bin/pypy
# wav_test.py - Vedant Kumar <vsk@berkeley.edu>

import wave
from markov import MarkovChain

if __name__ == '__main__':
        chain = MarkovChain(3)
        f = wave.open("heritage.wav", 'r')
        print "Loading data..."
        buf = []
        # Just load a few seconds of audio...
        nr_secs = 25
        nr_frames = nr_secs * f.getframerate()
        f.readframes(nr_frames)
        f.rewind()
        for k in xrange(nr_frames):
                buf.append(f.readframes(1))
        print "Building Markov chain..."
        chain.add_sequence(buf)
        gen = chain.walk()
        out = wave.open("output.wav", 'wb')
        print "Generating output..."
        out.setparams(f.getparams())
        for k in xrange(f.getnframes()):
                out.writeframes(next(gen))

