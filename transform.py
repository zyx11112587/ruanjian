import numpy as np
from pydub import AudioSegment

def convert_audio(input_file, output_file):
    try:
        # 加载音频文件
        audio = AudioSegment.from_file(input_file)

        # 转换为单声道、16位 PCM 和 16kHz
        audio = audio.set_channels(1)  # 单声道
        audio = audio.set_frame_rate(16000)  # 16kHz
        audio = audio.set_sample_width(2)  # 16位

        # 导出转换后的音频
        audio.export(output_file, format="wav", codec='pcm_s16le')
    except Exception as e:
        print(f"An error occurred: {e}")

# 示例使用
# input_path = r"separated\htdemucs\music_2_1\vocals.wav"  # 输入文件路径
# output_path = r"separated\htdemucs\music_2_1\vocals_1.wav"  # 输出文件路径
# convert_audio(input_path, output_path)  # 假设目标长度是以毫秒为单位