from scipy import signal
import math
import numpy as np
import matplotlib.pyplot as plt
import librosa
import IPython.display as ipd
from utils import * 

class SecondLowShelving():
    def __init__(self, fc, fs, g, boost):
        self.fc = fc
        self.fs = fs
        self.g = g
        self.boost = boost
    
    def get_k(self):
        return math.tan(math.pi * self.fc / self.fs)
    
    def get_v0(self):
        if self.boost:
            return math.pow(10, self.g/20) 
        else:
            print("cut")
            return math.pow(1/10, self.g/20)
    
    def get_den(self):
        k = self.get_k()
        v = self.get_v0()
        if self.boost:
            a1 = 2*(math.pow(k, 2) - 1) / (1 + math.sqrt(2)*k + math.pow(k, 2))
            a2 = (1 - math.sqrt(2)*k + math.pow(k, 2)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
        else:
            a1 = 2*(v*math.pow(k, 2) - 1) / (1 + math.sqrt(2 * v) * k + v*math.pow(k, 2))
            a2 = (1 - math.sqrt(2*v)*k + v*math.pow(k, 2)) / (1 + math.sqrt(2*v)*k + v*math.pow(k, 2))
        
        return [1, a1, a2]
    
    def get_num(self):
        k = self.get_k()
        v = self.get_v0()
        if self.boost:
            b0 = (1 + math.sqrt(2*v)*k + v*math.pow(k,2)) / (1 + math.sqrt(2)*k + math.pow(k,2))
            b1 = (2 * (v*math.pow(k,2) - 1)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
            b2 = (1 - math.sqrt(2*v)*k + v*math.pow(k,2)) / (1 + math.sqrt(2)*k + math.pow(k,2))
        else:
            b0 = (1 + math.sqrt(2)*k + math.pow(k,2))/(1 + math.sqrt(2*v)*k + v*math.pow(k, 2))
            b1 = (2*(math.pow(k,2)-1)) / (1 + math.sqrt(2*v)*k + v*math.pow(k, 2))
            b2 = (1 - math.sqrt(2)*k + math.pow(k,2))/(1 + math.sqrt(2*v)*k + v*math.pow(k, 2))
        return [b0, b1, b2]
                  
    def get_response(self):
        num = self.get_num()
        den = self.get_den()
        w, h = signal.freqz(num, den, fs = self.fs)
        return w, h
    

    def plot_response(self):
        w, h = self.get_response()
        fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(10, 10))
        ax[0].plot(w, np.abs(h))
        ax[0].grid(True)
        ax[0].set_title('Second Order Low Shelving Magnitude Response')
        ax[0].set_xlabel('Frequency')
        
        ax[1].plot(w, np.unwrap(np.angle(h)))
        ax[1].grid(True)
        ax[1].set_title('Second Order Low Shelving Phase Response')
        ax[1].set_xlabel('Frequency')
           
    def apply_effect(self, waveform):
        num = self.get_num()
        den = self.get_den()
        result = signal.lfilter(num, den, waveform)
        return  result
        
        
    def play_audio(self, waveform):
        result = self.apply_effect(waveform)
        ipd.Audio(result, rate=self.fs)


        
class SecondHighShelving():
    def __init__(self, fc, fs, g, boost):
        self.fc = fc
        self.fs = fs
        self.g = g
        self.boost = boost
    
    def get_k(self):
        return math.tan(math.pi * self.fc / self.fs)
    
    def get_v0(self):
        g = self.g
        if self.boost:
            return math.pow(10, g/20) 
        else:
            return math.pow(1/10, g/20)
    
    def get_den(self):
        k = self.get_k()
        v = self.get_v0()
        if self.boost:
            a1 = 2*(math.pow(k, 2) - 1) / (1 + math.sqrt(2)*k + math.pow(k, 2))
            a2 = (1 - math.sqrt(2)*k + math.pow(k, 2)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
        else:
            a1 = (2*(math.pow(k, 2)/v - 1))/(1 + math.sqrt(2/v)*k + math.pow(k,2)/v)
            a2 = (1 - math.sqrt(2/v)*k + math.pow(k,2)/v) / (1 + math.sqrt(2/v)*k + math.pow(k,2)/v)
        return [1, a1, a2]
    
    def get_num(self):
        k = self.get_k()
        v = self.get_v0()
        if self.boost:
            b0 = (v + math.sqrt(2*v)*k + math.pow(k, 2)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
            b1 = (2*(math.pow(k, 2) - v)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
            b2 = (v - math.sqrt(2*v)*k + math.pow(k, 2)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
        else:
            b0 = (1 + math.sqrt(2)*k + math.pow(k,2))/(v + math.sqrt(2*v)*k + math.pow(k,2))
            b1 = (2*(math.pow(k, 2) - 1))/(v + np.sqrt(2*v)*k + math.pow(k,2))
            b2 = (1 - math.sqrt(2)*k + math.pow(k,2))/(v + math.sqrt(2*v)*k + math.pow(k,2))
            
        return [b0, b1, b2]
                  
    def get_response(self):
        num = self.get_num()
        den = self.get_den()
        w, h = signal.freqz(num, den, fs = self.fs)
        return w, h
    

    def plot_response(self):
        w, h = self.get_response()
        fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(10, 10))
        ax[0].plot(w, np.abs(h))
        ax[0].grid(True)
        ax[0].set_title('First Order High Shelving Magnitude Response')
        ax[0].set_xlabel('Frequency')
        
        ax[1].plot(w, np.unwrap(np.angle(h)))
        ax[1].grid(True)
        ax[1].set_title('First Order High Shelving Phase Response')
        ax[1].set_xlabel('Frequency')
           
    def apply_effect(self, waveform):
        num = self.get_num()
        den = self.get_den()
        result = signal.lfilter(num, den, waveform)
        return  result
        
        
    def play_audio(self, waveform):
        result = self.apply_effect(waveform)
        ipd.Audio(result, rate=self.fs)

        
        
class SecondPeak():
    def __init__(self, fc, fs, fb, g, boost):
        self.fc = fc
        self.fs = fs
        self.fb = fb
        self.g = g
        self.boost = boost
    
    def get_k(self):
        return math.tan(math.pi * self.fc / self.fs)
    
    def get_d(self):
        return -math.cos(2*math.pi*self.fc/self.fs)
    
    def get_v0(self):
        if self.boost:
            return math.pow(10, self.g/20) 
        else:
            return math.pow(10, -self.g/20)
    
    def get_alpha(self):
        if self.boost:
            return (math.tan((math.pi * self.fb) / self.fs) - 1) / (math.tan((math.pi * self.fb) / self.fs) + 1)
        else:
            return (math.tan((math.pi * self.fb) / self.fs) - self.get_v0())/ ( math.tan((math.pi * self.fb) / self.fs) + self.get_v0())
    
    def get_num_den(self):
        alpha = self.get_alpha()
        d = self.get_d()
        h0 = self.get_v0() - 1
        num = [-alpha, d * (1 - alpha), 1]
        den = [1, d * (1 - alpha), -alpha]
        num = np.array(num)
        den = np.array(den)
        #############
        num = den - num
        num = h0 * num / 2
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
        ax[0].set_title('Second Order Peak Magnitude Response')
        ax[0].set_xlabel('Frequency')
        
        ax[1].plot(w, np.unwrap(np.angle(h)))
        ax[1].grid(True)
        ax[1].set_title('Second Order Peak Phase Response')
        ax[1].set_xlabel('Frequency')
           
    def apply_effect(self, waveform):
        num, den = self.get_num_den()
        result = signal.lfilter(num, den, waveform)
        return  result
        
    def play_audio(self, waveform):
        result = self.apply_effect(waveform)
        ipd.Audio(result, rate=self.fs)