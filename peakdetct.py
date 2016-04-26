import numpy as np

def locate_peaks(signal):
#function to find peaks
#a peak is any sample which is greater than its two nearest neighbours
    index = 0
    k = 2
    indices = []
    while k < len(signal) - 2:
        seg = signal[k-2:k+3]
        if np.amax(seg) < 150:
            k = k + 2
        else:
            if seg.argmax() == 2:
                indices.append(k)
                index = index + 1
                k = k + 2
        k += 1
    return indices


# def locate_peaks(signal):
# #function to find peaks
# #a peak is any sample which is greater than its two nearest neighbours
#     index = 0
#     num = 2
#     indices = []
#     for k in range(num,len(signal) - num):
#         seg = signal[k-num:k+num+1]
#         if seg.argmax() == num:
#             indices.append(k)
#             index = index + 1
#     return indices