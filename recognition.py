
# 示例使用
# audio_path = r"C:\Users\zhangyuxuan\PycharmProjects\pythonProject\ruanjian\ruanjian\separated\htdemucs\music_2_1\vocals_1.wav"  # 替换为音频文件路径
# model_path = r"C:\Users\zhangyuxuan\Desktop\wav\vosk-model-small-cn-0.22\vosk-model-small-cn-0.22"  # 替换为模型路径
# output_path =r"C:\Users\zhangyuxuan\Desktop\wav\output_2.txt"  # 替换为输出文件路径
# reduced_path=reduce_noise(audio_path)
# recognize_with_timestamps(reduced_path, model_path, output_path)

import wave
import json
from vosk import Model, KaldiRecognizer

# 检查模型路径
# model_path = r"C:\Users\zhangyuxuan\Desktop\wav\vosk-model-small-cn-0.22\vosk-model-small-cn-0.22"  # 替换为模型路径
# model = Model(model_path)
#
# # 输入音频文件路径
# vocal_audio_path = r"C:\Users\zhangyuxuan\PycharmProjects\pythonProject\ruanjian\ruanjian\separated\htdemucs\music_2_1\vocals_1.wav"
#
# # 读取音频文件
# wf = wave.open(vocal_audio_path, "rb")
#
# # 初始化识别器
# recognizer = KaldiRecognizer(model, wf.getframerate())
#
# # 存储识别结果
# results = []
# sample_rate = wf.getframerate()
# frame_duration = 4000 / sample_rate  # 每帧的持续时间（秒）
#
# # 逐帧识别
# while True:
#     data = wf.readframes(4000)
#     if len(data) == 0:
#         break
#     if recognizer.AcceptWaveform(data):
#         result = json.loads(recognizer.Result())
#         # 添加时间戳
#         results.append((result, wf.tell() / sample_rate))  # 当前帧的时间戳
#     else:
#         result = json.loads(recognizer.PartialResult())
#         # 处理部分结果（可选）
#         if 'text' in result:
#             results.append((result, wf.tell() / sample_rate))  # 当前帧的时间戳
#
# # 完成识别
# final_result = json.loads(recognizer.FinalResult())
# if 'text' in final_result:
#     results.append((final_result, wf.tell() / sample_rate))
#
# # 保存结果到文本文件
# output_file_path = r"C:\Users\zhangyuxuan\PycharmProjects\pythonProject\ruanjian\ruanjian\output.txt"
# with open(output_file_path, 'w', encoding='utf-8') as f:
#     for result, timestamp in results:
#         if 'text' in result and result['text']:
#             f.write(f"[{timestamp:.2f}s] {result['text']}\n")
#
# print(f"识别结果已保存到 {output_file_path}")

def recognize_with_timestamps(vocal_audio_path, model_path, output_file_path):
    model = Model(model_path)
    # 读取音频文件
    wf = wave.open(vocal_audio_path, "rb")

    # 初始化识别器
    recognizer = KaldiRecognizer(model, wf.getframerate())

    # 存储识别结果
    results = []
    sample_rate = wf.getframerate()
    frame_duration = 4000 / sample_rate  # 每帧的持续时间（秒）

    # 逐帧识别
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            # 添加时间戳
            results.append((result, wf.tell() / sample_rate))  # 当前帧的时间戳
        else:
            result = json.loads(recognizer.PartialResult())
            # 处理部分结果（可选）
            if 'text' in result:
                results.append((result, wf.tell() / sample_rate))  # 当前帧的时间戳

    # 完成识别
    final_result = json.loads(recognizer.FinalResult())
    if 'text' in final_result:
        results.append((final_result, wf.tell() / sample_rate))
    # 完成识别
    final_result = json.loads(recognizer.FinalResult())
    if 'text' in final_result:
        results.append((final_result, wf.tell() / sample_rate))

    # 保存结果到文本文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for result, timestamp in results:
            if 'text' in result and result['text']:
                f.write(f"[{timestamp:.2f}s] {result['text']}\n")

    print(f"识别结果已保存到 {output_file_path}")