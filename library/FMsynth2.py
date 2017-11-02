from com.jsyn.unitgen import UnitGenerator, SineOscillator, LineOut, UnitFilter
from com.jsyn.ports import UnitOutputPort
from music import *
from math import sin, pi
from gui import *
from array import array #Use arrays instead of lists (due to speed and efficiency) to copy and add the incoming input data with the output buffer of jSyn_AudioEngine
#from audio import LineOut

## Formula:   sin( 2*pi*Fc + B*sin( 2*pi*Fm) )     Fc:  Carrier Frequency     Fm:  Modulation Frequency    B:  Modulation Index (As B increases
## the modulation frequency steals energy from the carrier frequency)


class FMSynth(UnitFilter):

    def __init__(self, layers = 1, cFreq=220, mFreq=220, mIndex=1):
        print "FMSynth"

        self.numberOfOsc = layers          # number of Sine Oscillators used by synth
        self.carrierFrequency = cFreq      # carrier frequency for FM synthesizer
        self.modulationFrequency = mFreq   # modulation frequency for FM synthesizer
        self.modulationIndex = mIndex


        self.finalOutput = []              #Holds final synthesized sound

        self.carrierSineOscillatorArr = array('d')
        self.modulationSineOscillatorArr = array('d')


        #Build specified number of Sine Oscillators the FM synth will use
        self.newCarSineOsc = SineOscillator(self.carrierFrequency)
        self.newModSineOsc = SineOscillator(self.modulationFrequency)


        self.outputPort = UnitOutputPort(2,"Output")

        # create output port with enough output ports as there are input ports in jSyn_AudioEngine
        self.addPort(self.outputPort) #Make this port connectable to any module



    #Function called from internals of Jsyn that grab 8 float value chunks from the  jSyn_synthesizer
    def generate(self,start,limit):
        self.finalOutput = self.outputPort.getValues()
        self.modulationSineOscillatorArr = self.newModSineOsc.output.getValues()       #OutputMixingBlockPart is grabbing incoming data comeing through the jSyn_synthesizer
        self.carrierSineOscillatorArr = self.newCarSineOsc.output.getValues()          #Grabbing the Input buffer of the synthesisEngine

        #Do FM synthesis on each carrier and modulation sine oscillator pairs to get one full synthesized output
        for i in range(start,limit):
                self.finalOutput[i] += sin(2 * pi * self.carrierSineOscillatorArr[i] + self.modulationIndex * sin(2 * pi * self.modulationSineOscillatorArr[i])) #sin( 2*pi*Fc + B*sin( 2*pi*Fm) )


    def changeCarrierFrequency(self, newCFreq, layer=0):
        self.carrierFrequency = newCFreq
        self.sineOscList[layer].frequency.set(self.carrierFrequency)

    def changeModulationFrequency(self, newMFreq, layer=0):
        self.modulationFrequency = newMFreq

    def changeModulationIndex(self,newIndex):
        self.modulationIndex = newIndex

    #def getOutput(self):
    #    self.outputPort.output


if __name__ == '__main__':
    d = Display("FM Synthesizer", 300, 300)
    fmSynth = FMSynth()
    lineOut = LineOut()

    fmModulationIndex = Slider(VERTICAL, 0, 127, 0, fmSynth.changeModulationIndex)
    d.add(fmModulationIndex, 100, 100)

    fmSynth.output.connect(0, lineOut.input, 0)
    fmSynth.output.connect(0, lineOut.input, 1)

    jSyn.synth.add(fmSynth)
    jSyn.synth.add(lineOut)

    lineOut.start()
