from pydub import AudioSegment
import numpy as np


def reduce_noise(audio_file):
    # 读取音频文件
    sound = AudioSegment.from_file(audio_file)

    # 进行简单的降噪处理，比如削弱低频部分
    sound = sound.high_pass_filter(300)  # 300Hz高通滤波

    # 导出处理后的音频
    reduced_noise_file = audio_file.replace(".wav", "_reduced_noise.wav")
    sound.export(reduced_noise_file, format="wav")
    return reduced_noise_file
