import os
import sys  # 导入 sys 模块
import contextlib
import wave
import pydub
import numpy as np
import torch
torch.set_num_threads(1)


# 参数设置
sample_rate = 16000
min_buffer_duration = 0.6  # 这是音频缓冲区的最小长度，单位是秒
# 初始化 VAD
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              source='github')


def int2float(sound):
    abs_max = np.abs(sound).max()
    sound = sound.astype('float32')
    if abs_max > 0:
        sound *= 1/32768
    sound = sound.squeeze()  # depends on the use case
    return sound


def audio_to_wave(audio_path, target_path="temp.wav"):
    audio = pydub.AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1).set_frame_rate(sample_rate)
    audio.export(target_path, format="wav")


def frame_generator(frame_duration_s, audio, sample_rate):
    n = int(sample_rate * frame_duration_s * 2)  # 一帧的存储字节长度
    offset = 0  # 字节偏移量
    timestamp = 0.0  # 时间偏移量
    duration = frame_duration_s * 1000.0  # 单位毫秒
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


class Frame:
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes  # 此帧字节大小
        self.timestamp = timestamp  # 此帧开始时间，单位毫秒
        self.duration = duration  # 此帧的持续时间，单位毫秒


def vad_collector(frames, sample_rate):
    voiced_frames = []
    for frame in frames:
        audio_frame_np = np.frombuffer(frame.bytes, dtype=np.int16)
        audio_float32 = int2float(audio_frame_np)
        with torch.no_grad():
            new_confidence = model(torch.from_numpy(
                audio_float32), sample_rate).item()
        if new_confidence > 0.5:
            is_speech = True
        else:
            is_speech = False
        if is_speech:
            voiced_frames.append(frame)
        elif voiced_frames:
            start, end = voiced_frames[0].timestamp, voiced_frames[-1].timestamp + \
                voiced_frames[-1].duration
            voiced_frames = []
            yield start, end
    if voiced_frames:
        start, end = voiced_frames[0].timestamp, voiced_frames[-1].timestamp + \
            voiced_frames[-1].duration
        yield start, end


def merge_segments(segments, merge_distance=3000):
    merged_segments = []
    for start, end in segments:
        if merged_segments and start - merged_segments[-1][1] <= merge_distance:
            merged_segments[-1] = (merged_segments[-1][0], end)
        else:
            merged_segments.append((start, end))
    return merged_segments


def format_time(milliseconds):
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        sample_rate = wf.getframerate()
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


def write_wave(path, audio: np.ndarray, sample_rate):
    audio = audio.astype(np.int16)  # Converting to int16 type for WAV format
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)  # Mono channel
        wf.setsampwidth(2)  # 16 bits per sample
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())


def detect_speech_segments(audio_path, output_folder="output"):
    audio_to_wave(audio_path)
    pcm_data, sample_rate = read_wave("temp.wav")
    audio_np = np.frombuffer(pcm_data, dtype=np.int16)  # 将PCM数据转换为numpy数组
    frames = frame_generator(min_buffer_duration, pcm_data, sample_rate)
    segments = list(vad_collector(list(frames), sample_rate))
    merged_segments = merge_segments(segments)

    os.makedirs(output_folder, exist_ok=True)  # 确保输出文件夹存在
    for index, (start, end) in enumerate(merged_segments):
        start_sample = int(start * sample_rate / 1000)
        end_sample = int(end * sample_rate / 1000)
        segment_audio = audio_np[start_sample:end_sample]
        segment_path = os.path.join(
            output_folder, f"segment_{index+1}_{format_time(start)}-{format_time(end)}.wav")
        write_wave(segment_path, segment_audio, sample_rate)
        print(f"Speech segment saved: {segment_path}")


# 从命令行读取参数
if __name__ == "__main__":
        audio_file = r"C:\Users\zhangyuxuan\Desktop\wav\music_2_1.wav"
        output_folder = r"C:\Users\zhangyuxuan\Desktop\wav\seperated"
        detect_speech_segments(audio_file, output_folder)