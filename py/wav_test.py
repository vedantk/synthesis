#!/usr/bin/pypy
# wav_test.py - Vedant Kumar <vsk@berkeley.edu>

import wave
from markov import MarkovChain

if __name__ == '__main__':
        chain = MarkovChain(5)
        f = wave.open("heritage.wav", 'r')
        print "Loading data..."
        buf = []
        # Just load a few seconds of audio...
        for k in xrange(15 * f.getframerate()):
                buf.append(f.readframes(1))
        print "Building Markov chain..."
        chain.add_sequence(buf)
        gen = chain.walk()
        out = wave.open("output.wav", 'wb')
        print "Generating output..."
        out.setparams(f.getparams())
        for k in xrange(f.getnframes()):
                out.writeframes(next(gen))

