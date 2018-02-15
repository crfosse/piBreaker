import operator
import struct
import time
from scipy.signal import butter, lfilter, resample
import numpy as np
from subprocess import call

def filter(data, f1, f2, fs):
    nyq = 0.5*fs
    low = f1/nyq
    high = f2/nyq

    b, a = butter(5, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y



def delay_from_corr(set1, set2, fs, f1, f2):    
    y1 = filter(set1, f1, f2, fs)
    y2 = filter(set2, f1, f2, fs)

    xcorr = np.absolute(np.correlate(y1, y2, "full")) #absolute value?
    index, value = max(enumerate(xcorr), key=operator.itemgetter(1)) 
    sample_delay = (len(xcorr)+1)/2-1-index
    time_delay = float(sample_delay)/fs #in seconds
    #print "Value: %d, Index: %d" % (value, index)
    
    return time_delay

def read_from_bin(filepath, channels):
    sample_period = np.fromfile(filepath, dtype = "double", count=1,sep='')
    adc_data = np.fromfile(filepath, dtype="uint16", count=-1, sep='')
    adc_data = np.delete(adc_data,[0,1,2,3])

    len_data = len(adc_data) 
    samples = len_data/channels
    raw_data = np.zeros((samples,channels), dtype="uint16")
    for row in range(0, samples):
        for col in range(0, channels):
            raw_data[row, col] = adc_data[row*channels+col]
    return raw_data, sample_period

def angle_calculation(t1,t2,t3):
    if t1 == 0 and t2 == 0 and t3 == 0:
        return -1

    #if t1 -t2 -2*t3 == 0: 
    #    if t1 > 0: 
    #        return 270
    #    else: 
    #        return 90
    
    theta_rad = np.arctan2(1.1472*(t1+t2),(t1-t2-2*t3))
    theta = theta_rad*180/3.14

    #if t3 < 0:
    #    theta = theta + 180
    #if theta < 0: 
    #    theta = theta + 360
    
    return theta + 180

def sampling(channels, f1, f2):
     

    call("sudo ./adc_sampler 2500", shell=True)

    [raw_data, sample_period] = read_from_bin("adcData.bin", channels)

    fs = int(1/sample_period*10**6)

    channel1 = np.transpose(raw_data[:,0])
    channel2 = np.transpose(raw_data[:,1])
    channel3 = np.transpose(raw_data[:,2])
    
    

    N = 10000
    channel1 = resample(channel1, N)
    channel2 = resample(channel2, N)
    channel3 = resample(channel3, N)

    time_delay1 = delay_from_corr(channel2, channel1, fs, f1, f2)
    time_delay2 = delay_from_corr(channel3, channel1, fs, f1, f2)
    time_delay3 = delay_from_corr(channel3, channel2, fs, f1, f2)
    """
    print  time_delay1
    print  time_delay2
    print  time_delay3
    """

    theta = angle_calculation(time_delay1, time_delay2, time_delay3)
    
    return theta

def samplingRadar(channels, f1, f2):
    
    call("sudo ./adc_sampler 32768", shell=True) #2^15 samples

    [raw_data, sample_period] = read_from_bin("adcData.bin", channels)

    fs = int(1/sample_period*10**6)

    channel4 = np.transpose(raw_data[:,3])
    channel5 = np.transpose(raw_data[:,4])


    N = 10000
    channel4 = resample(channel4, N)
    channel5 = resample(channel5, N)
    
    return channel4, channel4

def main(measurementNr, realAngle):
    channels = 5
    f1 = 400
    f2 = 5000
    avg = 0
    N = 5
    angle_list = np.zeros((N,1), dtype=float)
    
    for i in range(0, N):
        theta = sampling(channels, f1, f2)
        print "Angle %i : %f" % (i, theta)
        angle_list[i] = theta

    avg = np.mean(angle_list)
    std = np.std(angle_list)

    print "Average: %f" % avg
    print "Std: %f" % std

    
    result_file = open("angle_meas_results.csv", "a")
    result_string = "%d, %f, %f, %f" % (measurementNr, realAngle, avg, std)
    for x in range(0,N): 
        result_string += ',%f' % angle_list[x]

    result_string += '\n'
    result_file.write(result_string)
    result_file.close()

def readRadar(measurementNr):
    
    channels = 5
    f1 = 400
    f2 = 5000
    
    channel4, channel5 = samplingRadar(channels, f1, f2)
    
    N = len(channel4)
    
    filename = "radar_sampling_nr_%d.csv" %measurementNr
    result_file = open(filename, "a")
    result_string = ""
    for x in range(0,N): 
        result_string += '%f, %f\n' % (channel4[x], channel4[x])

    result_file.write(result_string)
    result_file.close()

def fftRadarSampling(measurementNr):
    
    filename = "radar_sampling_nr_%d.csv" %measurementNr
    sampl_file = open(filename, "r")
    
    channel4 = []
    channel5 = []
    for line in sampl_file:
        numbers = line.split(', ')

        channel4.append(numbers[0])
        temp5 = numbers[1].replace('\n','')        
        channel5.append(temp5)

    channel4Complex = 1j*np.array(channel4, dtype=float)
    channel5 = np.array(channel5, dtype=float)
    spectrumComplex = np.fft.fft(channel4Complex + channel5)
    spectrumComplex[0] = 0 #Removing DC
    spectrumComplex[len(spectrumComplex)-1] = 0 #Removing high shit
    print float(np.argmax(spectrumComplex))/len(spectrumComplex) 
    print spectrumComplex
    print np.amax(spectrumComplex)

#readRadar(1)
#fftRadarSampling(1)

