import operator
import struct
from scipy.signal import butter, lfilter
from numpy import correlate


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

    xcorr = correlate(y1, y2, "full") #absolute value?
    index, value = max(enumerate(xcorr), key=operator.itemgetter(1)) 
    print xcorr
    sample_delay = (len(xcorr)+1)/2-1-index
    time_delay = float(sample_delay)/fs #in seconds
    print "Value: %d, Index: %d" % (value, index)
    print time_delay

def read_from_bin(filepath):
    raw_data = open(filepath, "rb")
    print raw_data.read() 
    
read_from_bin("ADC_sampling/adcData.bin")

"""
array1 = [0, 1, 2, 3, 4]
array2 = [1, 2, 3, 4, 0] 
fs = 1000
f1 = 1
f2 = 50
delay_from_corr(array1, array2, fs, f1, f2)
#filter(array1, 1, 100, 1000)
"""
