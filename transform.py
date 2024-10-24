import numpy as np
from pydub import AudioSegment

def convert_audio(input_file, output_file, target_length):
    try:
        # 加载音频文件
        audio = AudioSegment.from_file(input_file)

        # 转换为单声道、16位 PCM 和 16kHz
        audio = audio.set_channels(1)  # 单声道
        audio = audio.set_frame_rate(16000)  # 16kHz
        audio = audio.set_sample_width(2)  # 16位

        # 获取音频的样本数
        num_samples = len(audio.get_array_of_samples())

        # 检查样本长度
        if num_samples < target_length:
            # 用零填充
            audio = audio + AudioSegment.silent(duration=(target_length - num_samples) / audio.frame_rate)
        else:
            # 截断音频
            audio = audio[:target_length / audio.frame_rate]

        # 导出转换后的音频
        audio.export(output_file, format="wav")
    except Exception as e:
        print(f"An error occurred: {e}")

# 示例使用
input_path = r"C:\Users\zhangyuxuan\Desktop\wav\music_2.wav"  # 输入文件路径
output_path = r"C:\Users\zhangyuxuan\Desktop\wav\music_2_1.wav"  # 输出文件路径
convert_audio(input_path, output_path, 512 * 16000)  # 假设目标长度是以毫秒为单位