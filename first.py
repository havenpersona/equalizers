from scipy import signal
import math
import numpy as np
import matplotlib.pyplot as plt
import librosa
import IPython.display as ipd
import sympy as sy
from utils import * 

class FirstAllPass():
    def __init__(self, fc, fs, g, boost = True):
        self.fc = fc
        self.fs = fs
        self.g = g
        self.v_zero = math.pow(10, self.g/20)
        self.boost = boost
        
    def calc_alpha(self, boost = True):
        if boost:
            return (math.tan((math.pi * self.fc) / self.fs) - 1) / (math.tan((math.pi * self.fc) / self.fs) + 1)
        else:
            return(math.tan((math.pi * self.fc) / self.fs) - self.v_zero) / (math.tan((math.pi * self.fc) / self.fs) + self.v_zero)
    
    def calc_h_zero(self):
        return self.v_zero - 1
    
    
    def apply_effect(self, waveform):
        alpha = self.calc_alpha()
        h_zero = self.calc_h_zero()
        num = [alpha, 1]
        den = [1, alpha]
        result = signal.lfilter(num, den, waveform)
        return  result
    
    def get_num_den(self):
        alpha = self.calc_alpha()
        num = [alpha, 1]
        den = [1, alpha]
        return num, den
    
    def get_response(self):
        num, den = self.get_num_den()
        w, h = signal.freqz(num, den, fs = self.fs)
        return w, h
    
    def plot_response(self):
        w, h = self.get_response()
        
        fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(10, 10))
        ax[0].plot(w, np.abs(h))
        ax[0].grid(True)
        ax[0].set_title('First Order All Pass Magnitude Response')
        ax[0].set_xlabel('Frequency')
        ax[0].set_ylim([0, 3])
        ax[1].plot(w, np.unwrap(np.angle(h)))
        ax[1].grid(True)
        ax[1].set_title('First Order All Pass Phase Response')
        ax[1].set_xlabel('Frequency')
    
    def play_audio(self, waveform):
        result = self.apply_effect(waveform)
        ipd.Audio(result, rate=self.fs)
        

class FirstLowShelving():
    def __init__(self, fc, fs, g, boost):
        self.fc = fc
        self.fs = fs
        self.g = g
        self.boost = boost
    
    def get_v_zero(self):
        if self.boost:
            return math.pow(10, self.g/20)
        else:
            return math.pow(10, -self.g/20)
    
    def calc_alpha(self):
        if self.boost:
            return (math.tan((math.pi * self.fc) / self.fs) - 1) / (math.tan((math.pi * self.fc) / self.fs) + 1)
        else:
            return (math.tan((math.pi * self.fc) / self.fs) - self.get_v_zero()) / (math.tan((math.pi * self.fc) / self.fs) + self.get_v_zero())
    
    def calc_h_zero(self):
        return self.get_v_zero() - 1
    
    def get_num_den(self):
        alpha = self.calc_alpha()
        h_zero = self.calc_h_zero()
        num = np.array([alpha, 1])
        den = np.array([1, alpha])
        num = num + den
        num = num * h_zero / 2
        num = num + den
        return num, den
    
    def get_response(self):
        num, den = self.get_num_den()
        w, h = signal.freqz(num, den, fs = self.fs)
        return w, h
    
    def plot_response(self):
        w, h = self.get_response()
        fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(10, 10))
        ax[0].plot(w, np.abs(h))
        ax[0].grid(True)
        ax[0].set_title('First Order Low Shelving Magnitude Response')
        ax[0].set_xlabel('Frequency')
        ax[0].set_ylim([0, 3])
        ax[1].plot(w, np.unwrap(np.angle(h)))
        ax[1].grid(True)
        ax[1].set_title('First Order Low Shelving Phase Response')
        ax[1].set_xlabel('Frequency')
           
    def apply_effect(self, waveform):
        num, den = self.get_num_den()
        result = signal.lfilter(num, den, waveform)
        return  result
        
        
    def play_audio(self, waveform):
        result = self.apply_effect(waveform)
        ipd.Audio(result, rate=self.fs)
    
    
    
class FirstHighShelving():
    def __init__(self, fc, fs, g, boost = True):
        self.fc = fc
        self.fs = fs
        self.g = g
        self.boost = boost
    
    def get_v_zero(self):
        if self.boost:
            return math.pow(10, self.g/20)
        else:
            return math.pow(10, -self.g/20)
    def calc_alpha(self):
        if self.boost:
            return (math.tan((math.pi * self.fc) / self.fs) - 1) / (math.tan((math.pi * self.fc) / self.fs) + 1)
        else:
            return self.get_v_zero() * (math.tan((math.pi * self.fc) / self.fs) - 1) / (self.get_v_zero() * math.tan((math.pi * self.fc) / self.fs) + 1)
    
    def calc_h_zero(self):
        return self.get_v_zero() - 1
    
    def get_num_den(self):
        alpha = self.calc_alpha()
        h_zero = self.calc_h_zero()
        num = np.array([alpha, 1])
        den = np.array([1, alpha])
        num = den - num
        num = num * h_zero / 2
        num = num + den
        return num, den
    
    def get_response(self):
        num, den = self.get_num_den()
        w, h = signal.freqz(num, den, fs = self.fs)
        return w, h
    
    def plot_response(self):
        w, h = self.get_response()
        fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(10, 10))
        ax[0].plot(w, np.abs(h))
        ax[0].grid(True)
        ax[0].set_title('First Order High Magnitude Response')
        ax[0].set_xlabel('Frequency')
        ax[0].set_ylim([0, 3])
        ax[1].plot(w, np.unwrap(np.angle(h)))
        ax[1].grid(True)
        ax[1].set_title('First Order High Phase Response')
        ax[1].set_xlabel('Frequency')
           
    def apply_effect(self, waveform):
        num, den = self.get_num_den()
        result = signal.lfilter(num, den, waveform)
        return  result
        
        
    def play_audio(self, waveform):
        result = self.apply_effect(waveform)
        ipd.Audio(result, rate=self.fs)

