#!/usr/bin/pypy
# wav_test.py - Vedant Kumar <vsk@berkeley.edu>

import sys
import wave
from markov import MarkovChain

if __name__ == '__main__':
        if len(sys.argv) == 2:
                fname = sys.argv[1]
        else:
                fname = "heritage.wav"
        print fname

        chain = MarkovChain(3)
        f = wave.open(fname, 'r')
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
        out = wave.open("{0}-markov-output.wav".format(fname[:fname.find('.')), 'wb')
        print "Generating output..."
        out.setparams(f.getparams())
        for k in xrange(f.getnframes()):
                out.writeframes(next(gen))

