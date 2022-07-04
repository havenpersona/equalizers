from scipy import signal
import math
import numpy as np
import matplotlib.pyplot as plt
import librosa

class Utils():
    def __init__(self, order, f_type, boost):
        self.order = order
        self.f_type = f_type
        self.boost = boost
    
    def get_v0(self):
        g = self.g
        if self.boost:
            return math.pow(10, self.g/20)
        else:
            return math.pow(10, -self.g/20)
        
    def get_response(self):
        num, den = self.get_num_den()
        w, h = signal.freqz(num, den, fs = self.fs)
        return w, h
    
    def get_name(self):
        if self.boost:
            comp = 'boost'
        else:
            comp = 'cut'
        if self.f_type == 'allpass':
            name = self.order + " " + self.f_type
        else:
            name = self.order + " " + self.f_type + " " + comp
        return name
    def plot_response(self):
        w, h = self.get_response()
        fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(10, 10))
        print("the shape of w is ", w.shape)
        x = np.ones([h.shape[0], 1])
        ax[0].plot(w, np.abs(h))
        ax[0].plot(w, x, linestyle='--', color='red')
        ax[0].grid(True)
        ax[0].set_title(self.get_name() + ' Magnitude Response')
        ax[0].set_xlabel('Frequency')
        ax[0].set_ylim([0, 2])
        ax[1].plot(w, np.unwrap(np.angle(h)))
        ax[1].grid(True)
        ax[1].set_title(self.get_name() + ' Phase Response')
        ax[1].set_xlabel('Frequency')
           
    def apply_effect(self, waveform):
        num, den = self.get_num_den()
        result = signal.lfilter(num, den, waveform)
        return  result
         
    def play_audio(self, waveform):
        result = self.apply_effect(waveform)
        ipd.Audio(result, rate=self.fs)
        
    def get_k(self):
        return math.tan(math.pi * self.fc / self.fs)