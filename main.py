import subprocess

from ruanjian.ruanjian.get_notes import detect_notes, output_simplified_score
from ruanjian.ruanjian.load import load_audio
from ruanjian.ruanjian.recognition import recognize_with_timestamps
from ruanjian.ruanjian.transform import convert_audio

# 输入音频文件路径
input_audio_path = r"C:\Users\zhangyuxuan\Desktop\wav\music_5.wav"

# 使用 Demucs 分离音频
subprocess.run(['demucs', input_audio_path])

print("音频分离完成！")
# 示例使用
input_path = r"C:\Users\zhangyuxuan\PycharmProjects\pythonProject\ruanjian\ruanjian\separated\htdemucs\music_5\vocals.wav"  # 输入文件路径
output_path = r"C:\Users\zhangyuxuan\PycharmProjects\pythonProject\ruanjian\ruanjian\separated\htdemucs\music_5\vocals_1.wav"  # 输出文件路径
convert_audio(input_path, output_path)  # 假设目标长度是以毫秒为单位
model_path = r"C:\Users\zhangyuxuan\Desktop\wav\vosk-model-cn-0.22"  # 替换为模型路径
output_file_path=r"C:\Users\zhangyuxuan\Desktop\wav\output_5.txt"
recognize_with_timestamps(output_path, model_path, output_file_path)

audio_path = r"C:\Users\zhangyuxuan\Desktop\wav\music_5.wav"  # 替换为音乐文件路径
output_path_notes =  r"C:\Users\zhangyuxuan\Desktop\wav\note_5.txt" # 替换为输出文件路径

audio, sr = load_audio(audio_path)
notes = detect_notes(audio, sr)
output_simplified_score(notes, output_path_notes)
