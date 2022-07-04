from scipy import signal
import math
import numpy as np
import matplotlib.pyplot as plt
import librosa
import IPython.display as ipd
from utils import Utils

class SecondLowShelving(Utils):
    def __init__(self, fc, fs, g, order, f_type, boost = True):
        super().__init__(order, f_type, boost)
        self.fc = fc
        self.fs = fs
        self.g = g
        self.boost = boost
    
    def get_num_den(self):
        k = self.get_k()
        v = self.get_v0()
        if self.boost:
            b0 = (1 + math.sqrt(2*v)*k + v*math.pow(k,2)) / (1 + math.sqrt(2)*k + math.pow(k,2))
            b1 = (2 * (v*math.pow(k,2) - 1)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
            b2 = (1 - math.sqrt(2*v)*k + v*math.pow(k,2)) / (1 + math.sqrt(2)*k + math.pow(k,2))
        else:
            b0 = v*(1 + math.sqrt(2)*k + math.pow(k,2))/(v + math.sqrt(2*v)*k + math.pow(k, 2))
            b1 = (2*v*(math.pow(k,2)-1)) / (v + math.sqrt(2*v)*k + math.pow(k, 2))
            b2 = v*(1 - math.sqrt(2)*k + math.pow(k,2))/(v + math.sqrt(2*v)*k + math.pow(k, 2))
        if self.boost:
            a1 = 2*(math.pow(k, 2) - 1) / (1 + math.sqrt(2)*k + math.pow(k, 2))
            a2 = (1 - math.sqrt(2)*k + math.pow(k, 2)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
        else:
            a1 = 2*(math.pow(k, 2) - v) / (v + math.sqrt(2 * v) * k + math.pow(k, 2))
            a2 = (v - math.sqrt(2*v)*k + math.pow(k, 2)) / (v + math.sqrt(2*v)*k + math.pow(k, 2))
        num = [b0, b1, b2]
        den = [1, a1, a2]
        return num, den
    

        
class SecondHighShelving(Utils):
    def __init__(self, fc, fs, g, order, f_type, boost = True):
        super().__init__(order, f_type, boost)
        self.fc = fc
        self.fs = fs
        self.g = g
        self.boost = boost
    
    
    def get_num_den(self):
        k = self.get_k()
        v = self.get_v0()
        if self.boost:
            b0 = (v + math.sqrt(2*v)*k + math.pow(k, 2)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
            b1 = (2*(math.pow(k, 2) - v)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
            b2 = (v - math.sqrt(2*v)*k + math.pow(k, 2)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
        else:
            b0 = v*(1 + math.sqrt(2)*k + math.pow(k,2))/(1 + math.sqrt(2*v)*k + v*math.pow(k,2))
            b1 = (2*v*(math.pow(k, 2) - 1))/(1 + np.sqrt(2*v)*k + v*math.pow(k,2))
            b2 = v*(1 - math.sqrt(2)*k + math.pow(k,2))/(1 + math.sqrt(2*v)*k + v*math.pow(k,2))
        if self.boost:
            a1 = 2*(math.pow(k, 2) - 1) / (1 + math.sqrt(2)*k + math.pow(k, 2))
            a2 = (1 - math.sqrt(2)*k + math.pow(k, 2)) / (1 + math.sqrt(2)*k + math.pow(k, 2))
        else:
            a1 = (2*(v*math.pow(k, 2) - 1))/(1 + math.sqrt(2*v)*k + math.pow(k,2)*v)
            a2 = (1 - math.sqrt(2*v)*k + math.pow(k,2)*v) / (1 + math.sqrt(2*v)*k + math.pow(k,2)*v)
        num = [b0, b1, b2]
        den = [1, a1, a2]
        return num, den
    
class SecondPeak(Utils):
    def __init__(self, fc, fs, fb, g, order, f_type, boost = True):
        super().__init__(order, f_type, boost)
        self.fc = fc
        self.fs = fs
        self.fb = fb
        self.g = g
        self.boost = boost
    
    def get_d(self):
        return -math.cos(2*math.pi*self.fc/self.fs)
    
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
    

    
