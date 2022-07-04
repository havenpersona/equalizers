from scipy import signal
import math
import numpy as np
import matplotlib.pyplot as plt
import librosa
import IPython.display as ipd
from utils import Utils

class FirstAllPass(Utils):
    def __init__(self, fc, fs, g, order, f_type, boost = True):
        super().__init__(order, f_type, boost)
        self.fc = fc
        self.fs = fs
        self.g = g
        self.v0 = math.pow(10, self.g/20)
        self.boost = boost
        
    def get_alpha(self, boost = True):
        if boost:
            return (math.tan((math.pi * self.fc) / self.fs) - 1) / (math.tan((math.pi * self.fc) / self.fs) + 1)
        else:
            return(math.tan((math.pi * self.fc) / self.fs) - self.v0) / (math.tan((math.pi * self.fc) / self.fs) + self.v0)
    
    def get_h_zero(self):
        return self.v0 - 1
    
    def get_num_den(self):
        alpha = self.get_alpha()
        num = [alpha, 1]
        den = [1, alpha]
        return num, den
    
        

class FirstLowShelving(Utils):
    def __init__(self, fc, fs, g, order, f_type, boost = True):
        super().__init__(order, f_type, boost)
        self.fc = fc
        self.fs = fs
        self.g = g
        self.boost = boost
    
    def get_alpha(self):
        if self.boost:
            return (math.tan((math.pi * self.fc) / self.fs) - 1) / (math.tan((math.pi * self.fc) / self.fs) + 1)
        else:
            return (math.tan((math.pi * self.fc) / self.fs) - self.get_v0()) / (math.tan((math.pi * self.fc) / self.fs) + self.get_v0())
    
    def get_h_zero(self):
        return self.get_v0() - 1
    
    def get_num_den(self):
        alpha = self.get_alpha()
        h_zero = self.get_h_zero()
        num = np.array([alpha, 1])
        den = np.array([1, alpha])
        num = num + den
        num = num * h_zero / 2
        num = num + den
        return num, den
    
    
class FirstHighShelving(Utils):
    def __init__(self, fc, fs, g, order, f_type, boost = True):
        super().__init__(order, f_type, boost)
        self.fc = fc
        self.fs = fs
        self.g = g
        self.boost = boost
    
    def get_alpha(self):
        if self.boost:
            return (math.tan((math.pi * self.fc) / self.fs) - 1) / (math.tan((math.pi * self.fc) / self.fs) + 1)
        else:
            return self.get_v0() * (math.tan((math.pi * self.fc) / self.fs) - 1) / (self.get_v0() * math.tan((math.pi * self.fc) / self.fs) + 1)
    
    def get_h_zero(self):
        return self.get_v0() - 1
    
    def get_num_den(self):
        alpha = self.get_alpha()
        h_zero = self.get_h_zero()
        num = np.array([alpha, 1])
        den = np.array([1, alpha])
        num = den - num
        num = num * h_zero / 2
        num = num + den
        return num, den
    

    


