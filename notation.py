import librosa
import numpy as np
import matplotlib.pyplot as plt

# 音高到音名的映射
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def hz_to_note_name(hz):
    """将频率转换为音符名称（如 C4、D#4 等）。"""
    if hz == 0:
        return None  # 无声音频片段
    note = librosa.hz_to_note(hz)
    return note


def extract_notes(file_path, sample_interval=20):
    """提取音频文件中的音符名称，按给定的采样间隔抽取音符。"""
    # 加载音频文件
    y, sr = librosa.load(file_path)

    # 提取音高序列
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    # 收集音符
    notes = []

    for t in range(0, pitches.shape[1], sample_interval):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        note_name = hz_to_note_name(pitch)

        if note_name is not None:
            notes.append(note_name)

    return notes


def plot_notes(notes, notes_per_line=60, output_file='output.png', staff_spacing=1):
    """将音符序列绘制到五线谱上，并保存为图片。"""
    plt.figure(figsize=(60, 16))

    # 五线谱
    line_height = 6  # 每一行五线谱的高度
    total_lines = (len(notes) // notes_per_line) + 1

    for line in range(total_lines):
        base_y = line * (line_height + staff_spacing)  # 行基线位置
        for i in range(5):  # 每行五条线
            y = base_y + i  # 每条线的 y 位置
            plt.plot([0, notes_per_line], [y, y], 'k', lw=2)

    # 扩展的音符映射
    y_mapping = {
        'C3': -3, 'D3': -2.5, 'E3': -2, 'F3': -1.5, 'G3': -1, 'A3': -0.5, 'B3': 0,
        'C4': 0.5, 'D4': 1, 'E4': 1.5, 'F4': 2, 'G4': 2.5, 'A4': 3, 'B4': 3.5,
        'C5': 4, 'D5': 4.5, 'E5': 5
    }

    # 音符绘制
    for i, note in enumerate(notes):
        line = i // notes_per_line
        x = i % notes_per_line
        y = y_mapping.get(note, None)

        # 如果没有找到音符，跳过这个音符
        if y is None:
            continue  # 跳过该音符

        # 调整 y 坐标以适应不同的行和行间距
        y += line * (line_height + staff_spacing)
        plt.plot(x, y, 'bo', markersize=10)
        plt.text(x, y+0.4, note, ha='center', fontsize=8)

    plt.xlim(-1, notes_per_line)
    plt.ylim(-1, total_lines * (line_height + staff_spacing))
    plt.axis('off')

    # 保存为图片文件
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0.2)
    plt.show()


