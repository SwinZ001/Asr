import glob
import os

import hmmlearn.hmm as h1
import joblib
import wave as we
# 读取音频文件
import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pyplot as mp
import python_speech_features as sf

# fileName = r'E:\audio\wav\01.wav'
# # Wave = we.open(fileName)
# # # 获取总帧数
# # a = Wave.getparams().nframes
# # print('总帧数：',a)
# # # 获取采样频率
# # f = Wave.getparams().framerate
# # print('采样频率：',f)
# #
# # # 采样点的时间间隔
# # sample_time = 1/f
# # # 声音信号的长短
# # time = a/f
# # print(time)
# # 声音信号每一帧的大小
# sample_rate, audio_sequence = wf.read(fileName)
# print(sample_rate,audio_sequence)
# # x_seq = np.arange(0, time, sample_time)
# # print(x_seq, len(x_seq))
# # mp.plot(x_seq,audio_sequence,'blue')
# # mp.xlabel('time (s)')
# # mp.show()
#
#
# # 获取MFCC矩阵
# #提取特征维度（默认提取的特征维度是13）
# mfcc = sf.mfcc(audio_sequence,sample_rate)
# print(mfcc.shape)
# print(mfcc,len(mfcc),len(mfcc[0]))
#
# mp.matshow(mfcc.T,cmap = 'gist_rainbow')
# mp.show()



# 模型训练阶段
# 封装资源
def search_file(folders_way):
    # 存放资源字典
    audio_File_dict = {}
    # 获取当前文件路径下的文件夹名字
    folder_names = os.listdir(folders_way)
    for folder_name in folder_names:
        # 拼接当前文件夹下音频文件路径
        audio_way = os.path.join(folders_way,folder_name,'*')
        # 获取当前文件路径下的所有音频文件
        audio_res = glob.glob(audio_way)
        # 封装成字典
        audio_File_dict[folder_name] = audio_res
    return audio_File_dict

# 批量提取语音特征MFCC
def get_matrix(train_samples):
    train_x, train_y = [],[]
    for lable,filenames in train_samples.items():
        mfccs = np.array([])
        for filename in filenames:
            sample_rate, sigs = wf.read(filename)
            mfcc = sf.mfcc(sigs,sample_rate)
            if len(mfccs) == 0:
                mfccs = mfcc
            else:
                mfccs = np.append(mfccs, mfcc, axis=0)
        train_x.append(mfccs)
        train_y.append(lable)
    return train_x,train_y


# 制作语音模型
def model_train(train_x, train_y):
    models = {}
    for mfccs, lable in zip(train_x,train_y):
        model = h1.GaussianHMM(n_components=4,covariance_type='diag',n_iter=1000)
        models[lable] = model.fit(mfccs)
    return models


def make_Model():
    # 提取封装资源
    train_samples = search_file(r'E:\audio\wav')
    # 提取语音特征MFCC
    train_x,train_y = get_matrix(train_samples)
    # 制作语音模型
    models = model_train(train_x,train_y)
    # 保存语音模型
    joblib.dump(value=models,filename='wave.ckpt')


# 生成训练模型方法
make_Model()


# # 测试方法
# if __name__=="__main__":
#     test_samples = search_file(r'E:\audio\wav2')
#     test_x, test_y = get_matrix(test_samples)
#     models = joblib.load(filename='wave.ckpt')
#
#
#     def model_pred(test_x, test_y, models):
#         pred_test_y = []
#         for mfccs in test_x:
#             best_score, best_label = None, None
#             for label, model in models.items():
#                 score = model.score(mfccs)
#                 # print(score)
#                 if (best_score is None) or (best_score < score):
#                     best_score = score
#                     best_label = label
#                     # print (label best_label)
#             pred_test_y.append(best_label)
#         return pred_test_y
#
#
#     pred_test_y = model_pred(test_x, test_y, models)
#     print(pred_test_y)
#     print(test_y)