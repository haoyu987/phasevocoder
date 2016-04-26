import numpy as np

def resample(signal,pitchRatio):
    output_Length = int((len(signal)-1)/pitchRatio)
    output = np.zeros(output_Length)
    for i in range(output_Length-1):
        x = float(i*pitchRatio)
        ix = np.floor(x)
        dx = x - ix
        output[i] = signal[ix]*(1.0 - dx) + signal[ix+1]*dx
    return output
