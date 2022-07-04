from first import *
from second import *
import argparse




if __name__=="__main__":
    parser = argparse.ArgumentParser()
    my_args = parser.add_argument_group('Main')
    my_args.add_argument('--fc', type = int, help = 'cutoff frequency')
    my_args.add_argument('--fs', type = int, help = 'sampling rate')
    my_args.add_argument('--fb', type = int, help = 'bandwidth')
    my_args.add_argument('--g', type = int, help = 'gain')
    my_args.add_argument('--order', type = str, choices = ['first', 'second'])
    my_args.add_argument('--f_type', type = str, choices = ['allpass', 'low', 'high', 'peak'])
    parser.add_argument('--boost', type = str, choices = ['Yes', 'No'])
    my_args.add_argument('--path', type = str, help = 'the name of directory')
    my_args.add_argument('--audio_file', type = str, help = 'the name of audio file')
    my_args.set_defaults(fc = 2000,
        fs = 44100,
        fb = 100,
        g = 5,
        order = 'second',
        f_type = 'allpass',
        path = '/Users/user/Workspace/hw2_audio/',
        audio_file = 'suzanne.wav',
        boost = 'True'
    )
    args = parser.parse_args()
    
    if args.boost == 'Yes':
        boost = True
    else:
        boost = False

    first_allpass = FirstAllPass(fc = args.fc, fs = args.fs, g = args.g, order = args.order, f_type = args.f_type, boost = boost)
    first_low = FirstLowShelving(fc = args.fc, fs = args.fs, g = args.g, order = args.order, f_type = args.f_type, boost = boost)
    first_high = FirstHighShelving(fc = args.fc, fs = args.fs, g = args.g, order = args.order, f_type = args.f_type, boost = boost)
    #second_allpass = SecondAllPass(args.fc, args.fs, args.fb, args.g, boost)
    second_low = SecondLowShelving(fc = args.fc, fs = args.fs, g = args.g, order = args.order, f_type = args.f_type, boost = boost)
    second_high = SecondHighShelving(fc = args.fc, fs = args.fs, g = args.g, order = args.order, f_type = args.f_type, boost = boost)
    second_peak = SecondPeak(fc = args.fc, fs = args.fs, fb = args.fb, g = args.g, order = args.order, f_type = args.f_type, boost = boost)
    name = args.path + args.audio_file
    waveform, _ = librosa.load(name, sr = args.fs)
    
    if args.order == 'first':
        if args.f_type == 'allpass':
            first_allpass.plot_response()
        elif args.f_type == 'low':
            first_low.plot_response()
        elif args.f_type == 'high':
            first_high.plot_response()
        else:
            print("first order, not defined")
    if args.order == 'second':
        if args.f_type == 'allpass':
            second_allpass.plot_response()
        elif args.f_type == 'low':
            second_low.plot_response()
        elif args.f_type == 'high':
            second_high.plot_response()
        elif args.f_type == 'peak':
            second_peak.plot_response()
        else:
            print("second order, not defined")
