# ruanjian
软件工程作业：音频识谱  
tips:修改后主函数入口在in.py  
Python3.12无法修改UI界面，PyQt5tools最高支持Python3.9
***
分为两大部分：识别简谱和识别歌词
## 一、歌词识别
    1. 使用Demucs功能将完整的.wav音频文件分解为人声(vocal.wav)和伴奏
    2. 将分离的人声(vocal.wav)转化为识别模型要求的格式(单声道，16位 PCM 和 16kHz)
    3. 使用本地model(vosk-zh)进行识别输出歌词并打上时间戳(可改进，本地model识别正确率很低，可使用google speech recognition API实现，但是没钱)
    4. 输出歌词文件和对应时间戳
## 二、乐谱识别
    1. 使用librosa库实现，load载入音频，提取有效音高进行识别
    2. 将识别结果根据频率对应为相应的音符，转为简谱符号，找到调号
    3. 使用matplotlib.pyplot库将输出分割输出为简谱图片
***
### 需要安装：
    1. ffmpeg进行格式转化，安装到系统
    2. vosk中文语音模型，添加到wav文件夹
    3. 歌曲.wav格式，放在wav文件夹
    
[ffmpeg下载](https://www.gyan.dev/ffmpeg/builds/)  
选择合适压缩包下载后解压，将bin目录添加到系统路径
***
[vosk下载界面](https://alphacephei.com/vosk/models)  
选择中文模型下载解压到wav文件夹
默认需要较大的模型，下载小模型也可以，替换模型路径即可

