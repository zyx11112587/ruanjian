import subprocess

from ruanjian.get_notes import detect_notes, output_simplified_score
from ruanjian.load import load_audio
from ruanjian.recognition import recognize_with_timestamps
from ruanjian.transform import convert_audio
from ruanjian.Shazam import recognize_song_info

# 听歌识曲
song_path = r"wav\music_1.wav"
recognize_song_info(song_path)

# 输入音频文件路径
input_audio_path = r"wav/music_1.wav"
demucs_path = r"C:\Users\28598\AppData\Roaming\Python\Python312\Scripts\demucs.exe"
# 使用 Demucs 分离音频
subprocess.run([demucs_path, input_audio_path])

print("音频分离完成！")
# 歌词识别
input_path = r"separated\htdemucs\music_2\vocals.wav"  # 分离后的人声音频
output_path = r"separated\htdemucs\music_2\vocals_1.wav"  # 音频降噪，格式转化
convert_audio(input_path, output_path)  # 假设目标长度是以毫秒为单位
model_path = r"wav\vosk-model-en-us-0.22-lgraph\vosk-model-en-us-0.22-lgraph"  # 替换为模型路径
output_file_path=r"wav\output_1.txt" #输出歌词文本
recognize_with_timestamps(output_path, model_path, output_file_path)
# 乐谱识别
audio_path = r"wav\music_1.wav"  # 音乐文件输入路径
output_path_notes =  r"wav\note_1.txt" # 乐谱输出路径

audio, sr = load_audio(audio_path)
notes = detect_notes(audio, sr)
output_simplified_score(notes, output_path_notes)
