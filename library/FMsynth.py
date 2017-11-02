from com.jsyn.unitgen import SineOscillator
from music import *

## Formula:   sin( 2*pi*Fc + B*sin( 2*pi*Fm) )     Fc:  Carrier Frequency     Fm:  Modulation Frequency    B:  Modulation Index (As B increases
## the modulation frequency steals energy from the carrier frequency)


class FMSynth():

    def __init__(self, layers = 1, cFreq=220, mFreq=220, mIndex=1):
        print "Synth"

        self.numberOfOsc = layers
        self.carrierFrequency = cFreq
        self.modulationFrequency = mFreq
        self.modulationIndex = mIndex

        self.sineOscList = [] #List of sine oscillators so user can have multiple layers of FM synthesis for more complex sounds

        for x in range(self.numberOfOsc):
            newSineOsc = SineOscillator(self.carrierFrequency)
            self.sineOscList.append(newSineOsc)
