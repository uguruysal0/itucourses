from scipy.io import wavfile as wav
import wave
from scipy.io import loadmat
from scipy.signal import freqz
import numpy as np
import matplotlib.pyplot as plt

# read region
sigFile = wave.open('signal.wav')

sound = sigFile.readframes(-1)
sound = np.fromstring(sound,'Int16')
rate = sigFile.getframerate()

mat_file = loadmat('filter.mat')
filter_= mat_file["b"][0]
# read region ends

# custom data 
F8  = 8000.0
F9  = 9000.0
F10 = 10000.0
# custom data ends


def modulator(signal,freq):
    samples = np.arange(signal.shape[0])
    cos = np.cos( (freq*2.0*np.pi)*samples/rate)
    modulated = signal*cos
    return modulated
    
def demodulator(signal,freq,phase=0):
    samples = np.arange(signal.shape[0])
    cos_1 = np.cos( (freq*2.0*np.pi)*samples/rate + phase )
    demodulated = signal*cos_1
    # amplitude increase
    return demodulated*2

def write(signal,filename):
    toWrite = np.array(signal,'Int16')
    wav.write(filename,rate,toWrite)
    return

# meaningful parts of the signal
sound = sound[16000:70000]


# normalizer
normalizer = np.max(sound)
sound = sound / normalizer
#
# filter
sound_filtered = np.convolve(sound,filter_)
# wav.write("filtered.wav",rate,sound_filtered)
#filter ends

# modulation 
modulated_1 = modulator(sound_filtered,F8)
modulated_2 = modulator(sound_filtered,F9)
# modulation ends



# demodulation and filtering
# Phase = 300 for first demulator gives zero output
demodulated_1 = demodulator(modulated_1,F8+80)
demodulated_1_filtered = np.convolve(demodulated_1,filter_)
demodulated_2 = demodulator(modulated_2,F9+10) 
demodulated_2_filtered = np.convolve(demodulated_2,filter_)
#demofulation ends

# Save file 
write(demodulated_1_filtered*normalizer,'demodulated_1.wav')
write(demodulated_1_filtered*normalizer,'demodulated_2.wav')
# Save file ends

# plots
# plt.specgram(demodulated_1,Fs=rate)
# plt.show()

# plt.plot([i for i in range(demodulated_1_filtered.shape[0]) ],demodulated_1_filtered*normalizer)
# plt.plot([i for i in range(sound_filtered.shape[0]) ],sound_filtered*normalizer)
# plt.legend(['filtered','unfiltered'], loc='upper left')
# plt.show()