def realtimePitchshift(pitch_ratio):
    import wave
    import pyaudio
    import struct
    import time
    import numpy as np
    from peakdetct import locate_peaks
    from resample import resample

    num_channels = 1        # Number of channels
    Fs = 16000                 # Sampling rate (frames/second)
    duration = 8
    signal_length = duration * Fs
    width = 2               # Number of bytes per sample

    # define the window size, synthesis hop size, and analysis hop size
    window_size = 2048
    synthesis_hopsize = window_size/4
    analysis_hopsize = int(synthesis_hopsize/pitch_ratio)

    # signal blocks for procesynthesis_hopsizeing and output
    delta_phase = np.zeros(window_size/2+1)                  # delta phase
    syn_phase = np.zeros(window_size/2+1, dtype=complex)     # synthesis phase angle

    k = np.linspace(0, window_size/2, window_size/2+1)       # ramp
    last_phase = np.zeros(window_size/2+1)                   # last frame phase
    accum_phase = np.zeros(window_size/2+1)                  # accumulated phase
    current_frame = np.zeros(window_size/2+1)                
    expected_phase = k*2*np.pi*analysis_hopsize/window_size  # expected phase

    p = pyaudio.PyAudio()
    stream = p.open(format            = pyaudio.paInt16,
                    channels          = 1,
                    rate              = Fs,
                    input             = True,
                    output            = True,
                    frames_per_buffer = Fs/4)

    # window function
    win = np.hanning(window_size)

    # human voice frequency range 80 - 250 Hz
    k_min = int(20 * window_size/Fs)-1

    # get first chunk of input data
    indata  = np.zeros(4*analysis_hopsize+window_size)
    indata[0:window_size] = np.array(struct.unpack('h'*window_size,stream.read(window_size)))
    indata[window_size:] = np.array(struct.unpack('h'*4*analysis_hopsize,stream.read(4*analysis_hopsize)))

    blocksize = window_size+synthesis_hopsize
    dout = np.zeros(4*synthesis_hopsize+window_size)
    zpad = np.zeros(blocksize)                                # zero pad when reading new frames
    dataout = ''
    Ampmax = 2**15-1
    pk_indices = range(1025)

    print "start."
    # while True:
    for i in range(int((signal_length-window_size)/(analysis_hopsize*4))):

        # initialize the pointers
        read_pt = 0
        write_pt = 0
        while read_pt <= 4*analysis_hopsize:
            # analysis
            # take the spectra of the current window
            current_frame =  np.fft.rfft(win*indata[read_pt:read_pt+window_size])
            # current_frame[:k_min] = 0
            # current_frame[k_max:] = 0

            # take the phase difference of two consecutive window
            current_phase = np.angle(current_frame)
            current_magn = abs(current_frame)
            delta_phase = current_phase - last_phase
            last_phase = np.copy(current_phase)

            # subtract expected phase to get delta phase
            delta_phase -= expected_phase
            delta_phase = np.unwrap(delta_phase)

            # accumulate delta phase
            accum_phase[pk_indices] = accum_phase[pk_indices] + (delta_phase[pk_indices] + expected_phase[pk_indices])*synthesis_hopsize/analysis_hopsize

            # define the region of influence
            rotation_angle = accum_phase[pk_indices] - current_phase[pk_indices]
            start_point = 0

            for k in range(len(pk_indices)-1):
                peak = pk_indices[k]
                next_peak = pk_indices[k+1]
                end_point = int((peak + next_peak)/2)
                ri_indices = range(start_point,peak)+ range(peak+1,end_point)
                accum_phase[ri_indices] = rotation_angle[k] + current_phase[ri_indices]
                start_point = end_point

            # last peak
            ri_indices = range(start_point,next_peak)
            accum_phase[ri_indices] = rotation_angle[len(pk_indices)-1] + current_phase[ri_indices]
            
            # peak detect
            pk_indices = locate_peaks(current_magn)
            if len(pk_indices) == 0:
                pk_indices = [1]
            
            # synthesis
            syn_phase.real, syn_phase.imag = np.cos(accum_phase), np.sin(accum_phase)

            dout[write_pt:write_pt+window_size] += win*np.fft.irfft(current_magn*syn_phase)
            read_pt += analysis_hopsize
            write_pt += synthesis_hopsize

        output_frame = dout[0:blocksize]
        output_frame[output_frame>Ampmax] = Ampmax
        output_frame[output_frame<-Ampmax] = -Ampmax
        
        dataout = dataout + struct.pack('h'*len(output_frame), *list(output_frame))
        dout = np.concatenate((dout[blocksize:],zpad))
        indata[0:window_size-analysis_hopsize] = np.copy(indata[read_pt:])
        next_frame = stream.read(5*analysis_hopsize)

        # zero pad the last frame if necessary
        if len(next_frame) < 10*analysis_hopsize:
            zpad2 = np.zeros(5*analysis_hopsize-len(next_frame)/2)
            zpad2 = struct.pack('h'*len(zpad2), *list(zpad2))
            next_frame = next_frame+zpad2
        indata[window_size-analysis_hopsize:] = np.array(struct.unpack('h'*5*analysis_hopsize,next_frame))

        if len(dataout)/2 > Fs/pitch_ratio/4:
            samplen = len(dataout)/2
            resamp = resample(np.array(struct.unpack('h'*samplen,dataout)),pitch_ratio)
            output_data = struct.pack('h'*len(resamp), *list(resamp))
            stream.write(output_data)
            dataout = ''


    if len(dataout)/2 > 0:
        samplen = len(dataout)/2
        resamp = resample(np.array(struct.unpack('h'*samplen,dataout)),pitch_ratio)
        output_data = struct.pack('h'*len(resamp), *list(resamp))
        stream.write(output_data)

    print "done."

    stream.stop_stream()
    stream.close()
    p.terminate()
