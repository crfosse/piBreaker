import operator
import struct
from scipy.signal import butter, lfilter
import numpy as np
from matplotlib import pyplot as plt

def filter(data, f1, f2, fs):
    nyq = 0.5*fs
    low = f1/nyq
    high = f2/nyq

    b, a = butter(5, [low, high], btype='band')
    y = lfilter(b, a, data)  
    print y
    return y



def delay_from_corr(set1, set2, fs, f1, f2):    
    y1 = filter(set1, f1, f2, fs)
    y2 = filter(set2, f1, f2, fs)

    xcorr = np.correlate(y1, y2, "full") #absolute value?
    index, value = max(enumerate(xcorr), key=operator.itemgetter(1)) 
    print xcorr
    sample_delay = (len(xcorr)+1)/2-1-index
    time_delay = float(sample_delay)/fs #in seconds
    print "Value: %d, Index: %d" % (value, index)
    print time_delay

def read_from_bin(filepath, channels):
    sample_period = np.fromfile(filepath, dtype = "double", count=1,sep='')
    adc_data = np.fromfile(filepath, dtype="uint16", count=-1, sep='')
    len_data = len(adc_data) 
    samples = len_data/channels
    raw_data = np.zeros((samples,channels), dtype="uint16")
    for row in range(0, samples-1):
        for col in range(0, channels-1):
            raw_data[row, col] = adc_data[row*channels+col]
    plt.plot(raw_data)
    plt.show()
    print raw_data
    
read_from_bin("adcData.bin", 5)

"""
array1 = [0, 1, 2, 3, 4]
array2 = [1, 2, 3, 4, 0] 
fs = 1000
f1 = 1
f2 = 50
delay_from_corr(array1, array2, fs, f1, f2)
#filter(array1, 1, 100, 1000)
"""
