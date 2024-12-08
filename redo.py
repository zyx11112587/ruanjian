# 歌词识别
from ruanjian.get_notes import detect_notes, output_simplified_score
from ruanjian.load import load_audio
from ruanjian.recognition import recognize_with_timestamps
from ruanjian.transform import convert_audio

input_path = r"separated\htdemucs\music_1\vocals.wav"  # 分离后的人声音频
output_path = r"separated\htdemucs\music_1\vocals_1.wav"  # 音频降噪，格式转化
convert_audio(input_path, output_path)  # 假设目标长度是以毫秒为单位
model_path = r"wav\vosk-model-cn-0.22"  # 替换为模型路径
output_file_path=r"wav\output_1.txt" #输出歌词文本
recognize_with_timestamps(output_path, model_path, output_file_path)
# 乐谱识别
audio_path = r"wav\music_1.wav"  # 音乐文件输入路径
output_path_notes =  r"wav\note_1.txt" # 乐谱输出路径

audio, sr = load_audio(audio_path)
notes = detect_notes(audio, sr)
output_simplified_score(notes, output_path_notes)