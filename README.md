# phasevocoder
Phase Vocoder In Python
This module is based on PyGame and PyAudio.
![alt tag](https://github.com/haoyu987/phasevocoder/blob/master/docs/GUI.PNG)
![alttext](https://github.com/haoyu987/phasevocoder/blob/master/docs/GUI.PNG "Fig.1")
fig 1

Pitch shifting can be realized by simply changing the frame rate when playing the sound. But in this way, the length of the signal is also changed. So if we can scale the time of the signal while leave the pitch unchanged, we can get a pitch shifted version of the original sound with the same length.

![alt tag](https://github.com/haoyu987/phasevocoder/blob/master/docs/phasevocoder.png)
fig 2

## Time Scaling
Therefore, the most important part in pitch shifting becomes time scaling. To scale the time we can use different hop sizes when taking the STFT and inverse STFT. While the step size is scaled, the window size is identical. But we cannot just add the frames up in reconstruction. To reduce the discontinuity, we need some spectral processing. This technique is called phase vocoder. It consists of 3 stages: analysis, processing and synthesis.

![alt tag](https://github.com/haoyu987/phasevocoder/blob/master/docs/stretchsound.png)
fig 3

## Phase Correction
In frequency domain, a sound wave is interpreted as the magnitudes and phases of the frequencies. We usually don’t modify the magnitudes of the frequencies, as the magnitude represent the energy of a frequency component. So we only correct the phase.
![alt tag](https://github.com/haoyu987/phasevocoder/blob/master/docs/phase.png)
fig 4

## Phase Locking
In the phase correction process, there may be some frequencies near to each other, so the bins between them will be affected by both. In this case, the estimate of the true frequency may not be accurate.
Phase locking is a technique to reduce the artifacts resulting from this case. First, we locate the prominent peaks (the ones nearest to the true frequencies) by detecting the local maximums. And define the region of influence. For all the bins in the region, the phase change is the same as that of the peak.
![alt tag](https://github.com/haoyu987/phasevocoder/blob/master/docs/phaselock.png)
fig 5

For more detailed explanation, refer to the report in docs.

# Reference
1.	Florian Hammer, “Time-scale Modification using the Phase Vocoder”
2.	Joshua D. Reiss, Andrew P. McPherson, “Audio Effects Theory, Implementation and Application” Chapter 8 Phase Vocoder.
3.	Pitch Shifting Using The Fourier Transform
http://blogs.zynaptiq.com/bernsee/pitch-shifting-using-the-ft/
4.	Guitar Pitch shifter by François Grondin
http://www.guitarpitchshifter.com/algorithm.html#33
5.	A phase vocoder in python
https://audioprograming.wordpress.com/2012/03/02/a-phase-vocoder-in-python/
6.	Python, Pitch Shifting, and the Pianoputer
http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/
7.	miniGUI
http://cs.iupui.edu/~aharris/pygame/ch09/miniGUI.py

# special thanks
François Grondin's work, guitar pitch shifter, has been a great help to me when I did this project.

His website is here http://www.guitarpitchshifter.com/index.html

I have included some picture(fig)
