# coding=utf-8
# Author = 'QQ'

import numpy as np
import pandas as pd
import librosa

def mff_extract(filepath, n_fft=None, hop_length=None, n_mfcc=13,):
    y, sr = librosa.load(filepath, sr=None, mono=True, dtype=np.float32)
    nframes = y.shape[0]
    if sr != 44100:
        print "sr is not 44100, sr is %d" % sr

    power = 2
    if n_fft is None or hop_length is None:
        n_fft = sr / 25
        hop_length = sr / 100
    # compute power spectrum : frames-> windows -> stft
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length, center=False)) ** power

    # compute mel_spectrogram
    mel_basis = librosa.filters.mel(sr, n_fft)
    S = np.dot(mel_basis, S)

    # compute log_power_spectrogram and DCT transfrom
    S_db = librosa.power_to_db(S, ref_power=np.max)
    mfcc = np.dot(librosa.filters.dct(n_mfcc, S_db.shape[0]), S_db)

    # Calculate dynamic features
    deltea_mfcc = librosa.feature.delta(mfcc)
    deltea2_mfcc = librosa.feature.delta(mfcc, order=2)

    # combin mfcc
    M = np.vstack([mfcc, deltea_mfcc, deltea2_mfcc])
    return M.T

def str_to_array(string):
    string = string.strip('[')
    string = string.strip(']')
    string = string.strip()
    string = string.split(',')
    np_array = np.array([float(x) for x in string])
    return np_array

def upsampling(filepath, rate=10):
    raw_action = pd.read_csv(filepath)
    n_action = raw_action.shape[0]
    n_final_action = raw_action['totalTime'].sum() / rate
    start_pose = np.array([90, 90, 90, 90, 90, 90, 90, 60, 76, 110, 90, 90, 120, 104, 70, 90], dtype='float64')
    final_action = pd.DataFrame(columns=['s_1', 's_2', 's_3', 's_4', 's_5', 's_6', 's_7', 's_8',
                                         's_9', 's_10', 's_11', 's_12', 's_13', 's_14', 's_15', 's_16',
                                         'e_1', 'e_2', 'e_3', 'e_4', 'e_5', 'e_6', 'e_7', 'e_8', 'e_9', 'e_10',
                                         'e_11', 'e_12', 'e_13', 'e_14', 'e_15', 'e_16'])
    for i in range(n_action):
        run_time = raw_action.ix[i, "runTime"] / rate
        total_time = raw_action.ix[i, "totalTime"] / rate
        joint_angle = str_to_array(raw_action.ix[i, "jointAngle"])[:16]
        mean = (joint_angle - start_pose) / run_time
        for step in range(run_time - 1):
            end_pose = start_pose + mean
            final_action.loc[len(final_action)] = np.array([start_pose, end_pose]).reshape(-1)
            start_pose = end_pose
        end_pose = joint_angle
        final_action.loc[len(final_action)] = np.array([start_pose, end_pose]).reshape(-1)
        start_pose = end_pose
        if run_time < total_time:
            for step2 in range(total_time - run_time):
                final_action.loc[len(final_action)] = np.array([start_pose, end_pose]).reshape(-1)
    if n_final_action == len(final_action):
        print 'Up Sampling Successfully : the original action table has %d actions,' \
            ' the upsampling action table has %d actions' % (n_action, n_final_action)
    else:
        print 'Error: upsamping fail, because the number of final acitons is not equal to the total time'
    return final_action

def actions_frame(actions, win_time=4, hop_time=1):
    hop_time = 1  # 10 ms
    win_time = 4  # 40 ms
    action_frame = np.zeros((1 + (len(actions) - win_time) / hop_time, 32))
    stride = win_time - 1
    final_action = actions.as_matrix()
    action_frame[:, :16] = final_action[: action_frame.shape[0], :16]
    action_frame[:, 16:] = final_action[stride:, 16:]
    return action_frame




