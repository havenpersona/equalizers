class SecondLowShelving():
    def __init__(self, fc, fs, g, boost = True):
        self.fc = fc
        self.fs = fs
        self.g = g
        self.boost = boost
    
    def get_k(self):
        return math.tan(math.pi * self.fc / self.fs)
    
    def get_v0(self):
        if boost:
            return np.pow(10, self.g/20) 
        else:
            return np.pow(10, -self.g/20)
    
    def get_num(self):
        k = self.get_k()
        v = self.get_v0()
        if boost:
            a1 = 2(np.pow(k, 2) - 1) / (1 + math.sqrt(2)*k + np.pow(k, 2))
            a2 = (1 - math.sqrt(2)*k + np.pow(k, 2)) / (1 + math.sqrt(2)*k + np.pow(k, 2))
        else:
            a1 = 2(v*np.pow(k, 2) - 1) / (1 + math.sqrt(2 * v) * k + v*np.pow(k, 2))
            a2 = (1 - math.sqrt(2*v)*k + v*np.pow(k, 2)) / (1 + math.sqrt(2*v)*k + v*np.pow(k, 2))
        
        return [1, a1, a2]
    
    def get_den(self):
        k = self.get_k()
        v = self.get_v0()
        if boost:
            b0 = (1 + math.sqrt(2*v)*k + v*np.pow(k,2)) / (1 + math.sqrt(2)*k + np.pow(k,2))
            b1 = (2 * (v*np.pow(k,2) - 1) / (1 + math.sqrt(2)*k + np.pow(k, 2))
            b2 = (1 - math.sqrt(2*v)*k + v*np.pow(k,2)) / (1 + math.sqrt(2)*k + np.pow(k,2))
        else:
            b0 = 1 + math.sqrt(2)*k + np.pow(k,2)/(1 + math.sqrt(2*v)*k + v*np.pow(k, 2))
            b1 = (2*(math.pow(k,2)-1)) / (1 + math.sqrt(2*v)*k + v*np.pow(k, 2))
            b2 = 1 - math.sqrt(2)*k + np.pow(k,2)/(1 + math.sqrt(2*v)*k + v*np.pow(k, 2))
        return [b0, b1, b2]
                  
    def get_response(self):
        num = self.get_num()
        den = self.get_num()
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
        den = self.get_num()
        result = signal.lfilter(num, den, waveform)
        return  result
        
        
    def play_audio(self, waveform):
        result = self.apply_effect(waveform)
        ipd.Audio(result, rate=self.fs)
        