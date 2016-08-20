#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import errno
import os.path
import sys
import wave

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: %s long_wave textgrid wave_dir_out' % sys.argv[0]
        sys.exit(1)

    wave_in = wave.open(sys.argv[1], 'r')
    sampling_rate = wave_in.getframerate()
    sample_width = wave_in.getsampwidth()
    num_channels = wave_in.getnchannels()
    whole_num_frames = wave_in.getnframes()
    all_wave_data = wave_in.readframes(whole_num_frames)
    wave_in.close()

    text_grid = open(sys.argv[2], 'r')
    wav_info = text_grid.read().splitlines()
    text_grid.close()

    try:
        os.makedirs(sys.argv[3])
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(sys.argv[3]):
            pass
        else:
            raise

    num_intervals = 0
    line_begin = 0
    for info in wav_info:
        line_begin += 1
        if info.lstrip().startswith("intervals: size"):
            num_intervals = int(info.split()[-1])
            break
    #print line_begin

    voice_start = False
    intervals_info = wav_info[line_begin:line_begin + num_intervals*4]
    idx = 1
    for i in xrange(0, len(intervals_info), 4):
        xmin = float(intervals_info[i+1].split()[-1])
        xmax = float(intervals_info[i+2].split()[-1])
        #assert(xmin < xmax)
        text = intervals_info[i+3].split()[-1].replace('"', '').strip()
        if text == 'wrong':
            continue
        if text == '' and not voice_start:
            continue
        if not text == '' and text == '1':
            voice_start = True
        if voice_start:
            begin_pos = int(xmin*sampling_rate)*sample_width*num_channels
            end_pos = int(xmax*sampling_rate)*sample_width*num_channels
            name = os.path.basename(sys.argv[1])
            name = os.path.splitext(name)[0]
            index = '%05d' % idx
            wav_out = wave.open(os.path.join(sys.argv[3], name + '_' + index + '.wav'), 'w')
            wav_out.setparams([num_channels, sample_width, sampling_rate, 0, 'NONE', 'Noncompressed'])
            wav_out.writeframes(all_wave_data[begin_pos:end_pos])
            wav_out.close()
            idx += 1
        if not text == '' and text == '2':
            voice_start = False

