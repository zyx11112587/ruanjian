import subprocess

from ruanjian.ruanjian.recognition import recognize_with_timestamps
from ruanjian.ruanjian.transform import convert_audio

# 输入音频文件路径
input_audio_path = r"C:\Users\zhangyuxuan\Desktop\wav\music_3.wav"

# 使用 Demucs 分离音频
subprocess.run(['demucs', input_audio_path])

print("音频分离完成！")
# 示例使用
input_path = r"C:\Users\zhangyuxuan\PycharmProjects\pythonProject\ruanjian\ruanjian\separated\htdemucs\music_3\vocals.wav"  # 输入文件路径
output_path = r"C:\Users\zhangyuxuan\PycharmProjects\pythonProject\ruanjian\ruanjian\separated\htdemucs\music_3\vocals_1.wav"  # 输出文件路径
convert_audio(input_path, output_path)  # 假设目标长度是以毫秒为单位
model_path = r"C:\Users\zhangyuxuan\Desktop\wav\vosk-model-small-cn-0.22\vosk-model-small-cn-0.22"  # 替换为模型路径
output_file_path=r"C:\Users\zhangyuxuan\Desktop\wav\output.txt"
recognize_with_timestamps(output_path, model_path, output_file_path)