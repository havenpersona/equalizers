from first import *
import argparse




if __name__=="__main__":
    parser = argparse.ArgumentParser()
    my_args = parser.add_argument_group('Test')
    my_args.add_argument('--fc', type = int, help = 'cutoff frequency')
    my_args.add_argument('--fs', type = int, help = 'sampling rate')
    my_args.add_argument('--g', type = int, help = 'gain')
    my_args.add_argument('--order', type = str, choices = ['first', 'second'])
    my_args.add_argument('--f_type', type = str, choices = ['allpass', 'low_shelving', 'high_shelving', 'peak'])
    my_args.add_argument('--path', type = str, help = 'the name of directory')
    my_args.add_argument('--audio_file', type = str, help = 'the name of audio file')
    my_args.add_argument('--boost', type = bool, help = 'boost if true else cut')
    my_args.set_defaults(fc = 5000,
        fs = 44100,
        g = 10,
        order = 'second',
        f_type = 'allpass',
        path = '/Users/user/Workspace/hw2_audio/',
        audio_file = 'suzanne.wav'
    )
    args = parser.parse_args()
    
    #setattr(args, {
    #    'fc' == args.fc,
    #    'fs' == args.fs,
    #    'g' == args.g,
    #    'order' == args.order,
    #    'f_type' == args.f_type,
    #    'path' == args.path,
    #    'audio_file' == args.audio_file
    #})
    
    first_allpass = FirstAllPass(args.fc, args.fs, args.g, args.boost)
    first_low = FirstLowShelving(args.fc, args.fs, args.g, args.boost)
    first_high = FirstHighShelving(args.fc, args.fs, args.g, args.boost)
    
    name = args.path + args.audio_file
    waveform, _ = librosa.load(name, sr = args.fs)
    if args.order == 'first':
        if args.f_type == 'allpass':
            first_allpass.play_audio(waveform)
            first_allpass.plot_response()
        elif args.f_type == 'low_shelving':
            first_low.plot_response()
            #first_low.plot_response()
        elif args.f_type == 'high_shelving':
            first_high.plot_response()
            
    else:
        print("not defined, second order")
        
    