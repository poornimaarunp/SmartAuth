# -*- coding: utf-8 -*-
import numpy as np
from utils import reducenoise

def remove_silence(fs, signal,
        frame_duration = 0.02,
        frame_shift = 0.01,
        perc = 0.15):
    orig_dtype = type(signal[0])
    typeinfo = np.iinfo(orig_dtype)
    is_unsigned = typeinfo.min >= 0
    signal = signal.astype(np.int64)
    if is_unsigned:
        signal = signal - (typeinfo.max + 1) / 2

    siglen = len(signal) #signal length
    retsig = np.zeros(siglen, dtype = np.int64)
    frame_length = int(frame_duration * fs)
    frame_shift_length = int(frame_shift * fs)
    new_siglen = 0
    i = 0
    # NOTE: signal ** 2 where signal is a numpy array
    #       interpret an unsigned integer as signed integer,
    #       e.g, if dtype is uint8, then
    #           [128, 127, 129] ** 2 = [0, 1, 1]
    #       so the energy of the signal is somewhat
    #       right
    average_energy = np.sum(signal ** 2) / float(siglen) #normalizing the signal
#    print (average_energy)
    while i < siglen:
        subsig = signal[i:i + frame_length]
        ave_energy = np.sum(subsig ** 2) / float(len(subsig))
        if ave_energy < average_energy * perc:
            i += frame_length
        else:
            sigaddlen = min(frame_shift_length, len(subsig))
            retsig[new_siglen:new_siglen + sigaddlen] = subsig[:sigaddlen]
            new_siglen += sigaddlen
            i += frame_shift_length
    retsig = retsig[:new_siglen]
    if is_unsigned:
        retsig = retsig + typeinfo.max / 2
    return retsig.astype(orig_dtype)

def reduce_noise(fs,signal):
    noise_red = reducenoise.NoiseFilter()
    noise_red.init_noise(fs, signal)
    return noise_red.filter(fs,signal)

