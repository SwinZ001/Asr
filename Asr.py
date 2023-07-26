import wave
import scipy.io.wavfile as wf
import joblib
import numpy as np
import pyaudio
import os
import python_speech_features as sf
from make_Models import search_file, get_matrix

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# 设置音量配置
def dispose_Vol():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume

# 设置音量配置
def set_Vol(volume,subscript_value):
    # 获取当前音量值
    current_Vol = volume.GetMasterVolumeLevel()
    # 获取本机最大音量
    vr = volume.GetVolumeRange()
    if subscript_value == 1:
        max_vol = vr[subscript_value]
        # 设置音量(每次都比当前音量+5)
        volume.SetMasterVolumeLevel(current_Vol + 10, None)
        # 如果当前音量大于最大音量
        if current_Vol > max_vol:
            print('播放达到最大音量声音')
    elif subscript_value == 2:
        man_vol = vr[subscript_value]
        # 设置音量(每次都比当前音量+5)
        volume.SetMasterVolumeLevel(current_Vol - 10, None)
        # 如果当前音量大于最大音量
        if current_Vol < man_vol:
            print('播放达到最小音量声音')


# --------------------播放回答声音-----------------------
def answer():
    CHUNK = 1024
    wf = wave.open(r'E:\audio\回答\做尼.WAV', 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()
# --------------------语音识别-----------------------
def speech_recognition():
    test_samples = search_file(r'E:\audio\wav2')
    test_x, test_y = get_matrix(test_samples)
    models = joblib.load(filename='wave.ckpt')

    def model_pred(mfcc, test_y, models):
        pred_test_y = []
        for mfccs in mfcc:
            best_score, best_label = None, None
            for label, model in models.items():
                # 给语音打分
                score = model.score(mfccs)
                # print(score)
                if (best_score is None) or (best_score < score):
                    best_score = score
                    best_label = label
                    # print (label best_label)
            pred_test_y.append(best_label)
        return pred_test_y

    pred_test_y = model_pred(test_x, test_y, models)
    # print(pred_test_y)
    # print(test_y)
    return pred_test_y[0]


# --------------------录音-----------------------
def listen(select_i):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("录音开始")
    frames = []
    stat = True
    tempnum = 0
    while stat:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        print(tempnum)
        if (tempnum == 40):
            stat = False
        tempnum = tempnum + 1


    print("录音结束")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(r'E:\audio\wav2\01\01.wav', 'wb')  # 创建一个音频文件，名字为“01.wav"
    wf.setnchannels(CHANNELS)  # 设置声道数为2
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 设置采样深度为
    wf.setframerate(RATE)  # 设置采样率为16000
    # 将数据写入创建的音频文件
    wf.writeframes("".encode().join(frames))
    # 写完后将文件关闭
    wf.close()


    
#接收返回的语音识别结果
    speech_txt = speech_recognition()
    print(speech_txt)
    # 判断什么情况下的录音（1是唤醒）
    if select_i == 1:
        # 进行唤醒语音识别判断
        if speech_txt == '老肥老肥':
            os.remove(r'E:\audio\wav2\01\01.wav')
            # 符合则播放回答语音
            answer()
            # 执行唤醒后录音
            listen(2)
        else:
            listen(1)
    elif select_i == 2:
        # 进行唤醒后语音识别判断
        if speech_txt == '打开电视':
            print('执行打开电视操作')
            os.startfile('D:\日常\荐片\jianpian\jianpian.exe')
            os.remove(r'E:\audio\wav2\01\01.wav')
            listen(1)
        elif speech_txt == '静音':
            volume = dispose_Vol()
            volume.SetMute(1, None)
            os.remove(r'E:\audio\wav2\01\01.wav')
            listen(1)
        elif speech_txt == '大声点':
            volume = dispose_Vol()
            set_Vol(volume, 1)
            os.remove(r'E:\audio\wav2\01\01.wav')
            listen(1)
        elif speech_txt == '小声点':
            volume = dispose_Vol()
            set_Vol(volume, 0)
            os.remove(r'E:\audio\wav2\01\01.wav')
            listen(1)
        else:
            listen(1)







if __name__=="__main__":
    #   执行唤醒录音
    listen(1)






