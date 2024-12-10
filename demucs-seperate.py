import subprocess
# 输入音频文件路径
input_audio_path = r"wav\music_1.wav"

# 使用 Demucs 分离音频
subprocess.run(['C:\\Users\\28598\\AppData\\Roaming\\Python\\Python312\\Scripts\\demucs.exe', input_audio_path])

print("音频分离完成！")
