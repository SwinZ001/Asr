from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

# 获取当前音量值，0.0代表最大，-65.25代表最小
vl = volume.GetMasterVolumeLevel()
print(vl)

# 获取音量范围，我的电脑经测试是(-65.25, 0.0, 0.75)，第一个代表最小值，第二个代表最大值，第三个是增量。
# 也就是音量从大到小是0.0dB到-65.25dB这个范围，增量或者步长应为0.75dB
vr = volume.GetVolumeRange()

#
# 设置音量, 比如-13.5代表音量是40，0.0代表音量是100
volume.SetMasterVolumeLevel(-13.5, None)
# # volume.SetMasterVolumeLevel(-65.25, None)
# # volume.SetMasterVolumeLevel(0.0, None)
#
# # 判断是否静音，mute为1代表是静音，为0代表不是静音
# mute = volume.GetMute()
# print(mute)
#
# if volume.GetMasterVolumeLevel() == -65.25:
#     volume.SetMute(1, None)
# else:
#     volume.SetMute(0, None)
volume.SetMute(1, None)