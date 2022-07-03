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

    first_allpass = FirstAllPass(args.fc, args.fs, args.g, boost)
    first_low = FirstLowShelving(args.fc, args.fs, args.g, boost)
    first_high = FirstHighShelving(args.fc, args.fs, args.g, boost)
    #second_allpass = SecondAllPass(args.fc, args.fs, args.fb, args.g, boost)
    second_low = SecondLowShelving(args.fc, args.fs, args.g, boost)
    second_high = SecondHighShelving(args.fc, args.fs, args.g, boost)
    second_peak = SecondPeak(args.fc, args.fs, args.fb, args.g, boost)
    name = args.path + args.audio_file
    waveform, _ = librosa.load(name, sr = args.fs)
    
    if args.order == 'first':
        if args.f_type == 'allpass':
            first_allpass.play_audio(waveform)
            first_allpass.plot_response()
        elif args.f_type == 'low':
            first_low.plot_response()
        elif args.f_type == 'high':
            first_high.plot_response()
        else:
            print("not defined, first order")
    if args.order == 'second':
        if args.f_type == 'allpass':
            second_allpass.play_audio(waveform)
            second_allpass.plot_response()
        elif args.f_type == 'low':
            second_low.plot_response()
        elif args.f_type == 'high':
            second_high.plot_response()
        elif args.f_type == 'peak':
            second_peak.plot_response()
        else:
            print("not defined, second order anyway")
