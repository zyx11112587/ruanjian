import numpy as np
import librosa

from ruanjian.load import load_audio
#乐谱识别部分

def detect_notes(audio, sr):
    # 提取音高
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)

    # 获取音符及其对应的时间戳
    notes = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:  # 只考虑有效的音高
            time = librosa.frames_to_time(t, sr=sr)
            notes.append((pitch, time))

    return notes

def output_simplified_score(notes, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for pitch, time in notes:
            # 转换音高为简谱（可根据需求进行自定义）
            # 示例：将频率转换为音符（需要根据实际情况进行处理）
            note = librosa.hz_to_note(pitch)
            f.write(f"{note}: {time:.2f}s\n")

# 示例使用
# audio_path = r"wav\music_1.wav"  # 替换为音乐文件路径
# output_path =  r"wav\note.txt" # 替换为输出文件路径
#
# audio, sr = load_audio(audio_path)
# notes = detect_notes(audio, sr)
# output_simplified_score(notes, output_path)

