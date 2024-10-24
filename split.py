import librosa
import soundfile as sf
def extract_vocals(file_path, output_path):
    # 加载音频文件
    y, sr = librosa.load(file_path, sr=None)

    # 使用 librosa 分离人声
    vocals = librosa.effects.hpss(y)[0]  # 提取人声
    sf.write(output_path, vocals, sr)
extract_vocals(r"C:\Users\zhangyuxuan\Desktop\wav\music_2_1.wav",r"C:\Users\zhangyuxuan\Desktop\wav\music_2_1_1.wav")