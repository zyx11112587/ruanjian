import librosa
#载入音频
def load_audio(file_path):
    # 加载音频文件，sr=None保留原始采样率
    audio, sr = librosa.load(file_path, sr=None)
    return audio, sr
