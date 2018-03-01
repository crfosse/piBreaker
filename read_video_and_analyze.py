"""
Read the input video file, display first frame and ask the user to select a
region of interest.  Will then calculate the mean of each frame within the ROI,
and return the means of each frame, for each color channel, which is written to
file.

Similar to read_video_and_extract_roi.m, but for Python.

Requirements:

* Probably ffmpeg. Install it through your package manager.
* numpy
* OpenCV python package.
    For some reason, the default packages in Debian/Raspian (python-opencv and
    python3-opencv) seem to miss some important features (selectROI not present
    in python3 package, python2.7 package not compiled with FFMPEG support), so
    install them (locally for your user) using pip:
    - pip install opencv-python
    - (or pip3 install opencv-python)
"""
import sys
import cv2
import numpy as np

#CLI options
if len(sys.argv) < 2:
    print("Select smaller ROI of a video file, and save the mean of each image channel to file, one column per color channel (R, G, B), each row corresponding to a video frame number.")
    print("")
    print("Usage:\npython " + sys.argv[0] + " [path to input video file] [path to output data file]")
    exit()
filename = sys.argv[1]

#read video file
cap = cv2.VideoCapture(filename, cv2.CAP_FFMPEG)
if not cap.isOpened():
    print("Could not open input file. Wrong filename, or your OpenCV package might not be built with FFMPEG support. See docstring of this Python script.")
    exit()

num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

red_signal = np.zeros(num_frames)
green_signal = np.zeros(num_frames)
blue_signal = np.zeros(num_frames)

#loop through the video
count = 0
while cap.isOpened():
    ret, frame = cap.read() #'frame' is a normal numpy array of dimensions [height, width, 3], in order BGR
    if not ret:
        break

    #display window for selection of ROI
    if count == 0:
        frame_width = frame.shape[0]
        frame_height = frame.shape[1]
        crop_size = 128
        ROI = [int((frame_width - crop_size) / 2), int((frame_height - crop_size)/2),crop_size,crop_size]
        print("Looping through video.")

    #calculate mean
    cropped_frame = frame[ROI[1]:ROI[1] + ROI[3], ROI[0]:ROI[0] + ROI[2], :]
    colors = np.mean(cropped_frame, axis=(0,1))
    red_signal[count] = colors[2]
    green_signal[count] = colors[1]
    blue_signal[count] = colors[0]
    
    print("Frame " + str(count + 1) + "/" + str(num_frames), end="\r")
    count += 1

print()
cap.release()

red_fft = np.abs(np.fft.fft(red_signal))
green_fft = np.abs(np.fft.fft(green_signal))
blue_fft = np.abs(np.fft.fft(blue_signal))

red_peak_index = np.argmax(red_fft)
red_bmp = red_peak_index/len(red_fft) * fps/(2*np.pi) *60
print(red_bmp)


#save to file in order R, G, B.
np.savetxt('red_signal.txt', red_signal)
np.savetxt('green_signal.txt', green_signal)
np.savetxt('blue_signal.txt', blue_signal)

np.savetxt('red_fft.txt', red_fft)
np.savetxt('green_fft.txt', green_fft)
np.savetxt('blue_fft.txt', blue_fft)
print('fps: ' + str(fps))
#print("Data saved to '" + output_filename + "', fps = " + str(fps) + " frames/second")
