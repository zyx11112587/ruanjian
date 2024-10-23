import sys
import wave
import json
from vosk import Model, KaldiRecognizer

def recognize_with_timestamps(audio_file, model_path, output_file):
    # 加载模型
    model = Model(model_path)
    rec = KaldiRecognizer(model, 16000)

    # 打开音频文件
    wf = wave.open(audio_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        print("音频文件必须是单声道16-bit PCM格式的16kHz采样率")
        sys.exit(1)

    timestamps = []

    # 进行识别
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if 'result' in result:
                timestamps.extend(result['result'])
        else:
            partial_result = json.loads(rec.PartialResult())
            if 'result' in partial_result:
                timestamps.extend(partial_result['result'])

    # 处理最后的结果
    final_result = json.loads(rec.FinalResult())
    if 'result' in final_result:
        timestamps.extend(final_result['result'])

    # 将带有时间戳的文本信息写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in timestamps:
            word = item['word']
            start_time = item['start']
            end_time = item['end']
            f.write(f"{word}: {start_time:.2f}s - {end_time:.2f}s\n")

# 示例使用
audio_path = r"C:\Users\zhangyuxuan\Desktop\wav\music_1_1.wav"  # 替换为音频文件路径
model_path = r"C:\Users\zhangyuxuan\Desktop\wav\vosk-model-small-cn-0.22\vosk-model-small-cn-0.22"  # 替换为模型路径
output_path =r"C:\Users\zhangyuxuan\Desktop\wav\output.txt"  # 替换为输出文件路径
recognize_with_timestamps(audio_path, model_path, output_path)
