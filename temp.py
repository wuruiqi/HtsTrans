# coding=utf-8
# Author = 'QQ'


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import preprocess
audio_path = '3.mp3'
action_path = '3.csv'
mfcc = preprocess.mff_extract(audio_path)
actions = preprocess.upsampling(action_path)
action_frame = preprocess.actions_frame(actions)
action_filled = np.pad(action_frame, ((0, mfcc.shape[0]-action_frame.shape[0]), (0, 0)), 'edge')
sample = np.hstack([mfcc, action_filled])
np.savetxt('3.txt', sample)
sample = np.loadtxt('3.txt')
# 以上为数据预处理代码


actions.to_csv('actions.csv')
action_frame = pd.DataFrame(action_frame.T)
action_frame.to_csv('action_frame.csv')








# stft detail

# By default, use the entire frame

win_length = n_fft
window='hann'
dtype = np.complex64
pad_mode = 'reflect'

fft_window = librosa.filters.get_window(window, win_length, fftbins=True)
# Pad the window out to n_fft size
fft_window = librosa.util.pad_center(fft_window, n_fft)

# Reshape so that the window can be broadcast
fft_window = fft_window.reshape((-1, 1))

# Pad the time series so that frames are centered
y1 = np.pad(y1, int(n_fft//2), mode=pad_mode)

frames = librosa.util.frame(y1, frame_length=n_fft, hop_length=hop_length)
stft_matrix = np.empty((int(1 + n_fft // 2), frames.shape[1]), dtype=dtype, order='F')
# how many columns can we fit within MAX_MEM_BLOCK?
n_columns = int(librosa.util.MAX_MEM_BLOCK / (stft_matrix.shape[0] *
                                      stft_matrix.itemsize))

for bl_s in range(0, stft_matrix.shape[1], n_columns):
    bl_t = min(bl_s + n_columns, stft_matrix.shape[1])

    # RFFT and Conjugate here to match phase from DPWE code
    stft_matrix[:, bl_s:bl_t] = fft.fft(fft_window *
                                        frames[:, bl_s:bl_t],
                                        axis=0)[:stft_matrix.shape[0]].conj()


mfcc = librosa.feature.mfcc(y1, sr=sr, n_mfcc=13, )
n_fft = 441
hop_length = 512
D = librosa.stft(y1, n_fft=n_fft,  center=False)
n_fft = 512
hop_length = 128
D1 = librosa.stft(y1, n_fft=n_fft, hop_length=hop_length, center=False)
plt.figure()
plt.subplot(2, 1, 1)
librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), sr=sr*4,y_axis='log', x_axis='time')
#librosa.display.specshow(S, y_axis='log', x_axis='time')
plt.title('power spectogram')
plt.colorbar(format='%+2.0f db')
plt.subplot(2, 1, 2)
librosa.display.specshow(librosa.amplitude_to_db(D1, ref=np.max), sr=sr*4,y_axis='log', x_axis='time')
plt.title('power spectogram')
plt.colorbar(format='%+2.0f db')
plt.tight_layout()


plt.figure()
plt.subplot(2, 1, 1)
librosa.display.specshow(S_m, sr=sr, y_axis='log')
plt.colorbar()
plt.title('Power spectrogram')
plt.subplot(2, 1, 2)
librosa.display.specshow(S_db, sr =sr, y_axis = 'log', x_axis = 'time')
plt.colorbar(format='%+2.0f dB')
plt.title('Log-Power spectrogram')
plt.tight_layout()

plt.figure()
plt.subplot(3, 1, 1)
librosa.display.waveplot(y, sr=rate)
plt.title('Monophonic')
