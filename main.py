# import os
# import subprocess
# import sys
# from PyQt5.QtWidgets import QApplication, QDialog
# from PyQt5.QtCore import QThread, pyqtSignal
# from ruanjian.get_notes import detect_notes, output_simplified_score
# from ruanjian.load import load_audio
# from ruanjian.recognition import recognize_with_timestamps
# from ruanjian.transform import convert_audio
# from ruanjian.QtTest import Ui_Dialog
# import webbrowser  # 用于打开文件
#
#
# class WorkerThread(QThread):
#     # 定义完成操作后的信号
#     finished = pyqtSignal(str)
#
#     def __init__(self, task, *args):
#         super().__init__()
#         self.task = task
#         self.args = args
#
#     def run(self):
#         try:
#             print(1)
#             # 执行传入的任务函数
#             self.task(*self.args)
#         except Exception as e:
#             print(f"Error in {self.task.__name__}: {e}")
#         finally:
#             print(1)
#             # 发出完成信号，传递操作名称（或结果）
#             self.finished.emit(self.task.__name__)
#
#
# class MainWindow(QDialog, Ui_Dialog):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)  # 设置 UI 布局
#
#         # 为按钮添加点击事件
#         self.pushButton_1.clicked.connect(self.pushButton_1_clicked)
#         self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
#         self.pushButton_3.clicked.connect(self.pushButton_3_clicked)
#
#         # 取消按钮处理
#         self.buttonBox.rejected.connect(self.close)  # 点击 Cancel 按钮关闭对话框
#
#     def disable_buttons(self):
#         """禁用所有按钮"""
#         self.pushButton_1.setEnabled(False)
#         self.pushButton_2.setEnabled(False)
#         self.pushButton_3.setEnabled(False)
#
#     def enable_buttons(self):
#         """启用所有按钮"""
#         self.pushButton_1.setEnabled(True)
#         self.pushButton_2.setEnabled(True)
#         self.pushButton_3.setEnabled(True)
#
#     def pushButton_1_clicked(self):
#         print("开始分离音频...")
#         self.disable_buttons()
#
#         # 创建一个新的线程来执行音频分离任务
#         worker = WorkerThread(self.separate_audio, r"wav\music_1.wav")
#         worker.finished.connect(self.task_finished)
#         worker.start()
#
#     def separate_audio(self, input_audio_path):
#         """音频分离任务"""
#         try:
#             subprocess.run(['demucs', input_audio_path], check=True)
#             print("音频分离完成！")
#         except subprocess.CalledProcessError as e:
#             print(f"音频分离失败: {e}")
#         except Exception as e:
#             print(f"音频分离发生未知错误: {e}")
#
#     def pushButton_2_clicked(self):
#         print("输出歌词...")
#         self.disable_buttons()
#
#         # 创建一个新的线程来执行歌词识别任务
#         worker = WorkerThread(self.output_lyrics, r"separated\htdemucs\music_1\vocals.wav",
#                               r"separated\htdemucs\music_1\vocals_1.wav")
#         worker.finished.connect(self.task_finished)
#         worker.start()
#
#     def output_lyrics(self, input_path, output_path):
#         """歌词识别任务"""
#         try:
#             convert_audio(input_path, output_path)
#             model_path = r"wav\vosk-model-cn-0.22"
#             output_file_path = r"wav\output_1.txt"
#             recognize_with_timestamps(output_path, model_path, output_file_path)
#             print("歌词识别完成！")
#         except Exception as e:
#             print(f"歌词识别失败: {e}")
#
#         try:
#             # 打开输出文件
#             webbrowser.open(output_file_path)
#         except Exception as e:
#             print(f"打开输出文件失败: {e}")
#
#     def pushButton_3_clicked(self):
#         print("输出乐谱...")
#         self.disable_buttons()
#
#         # 创建一个新的线程来执行乐谱识别任务
#         worker = WorkerThread(self.output_score, r"wav\music_1.wav", r"wav\note_1.txt")
#         worker.finished.connect(self.task_finished)
#         worker.start()
#
#     def output_score(self, audio_path, output_path_notes):
#         """乐谱识别任务"""
#         try:
#             audio, sr = load_audio(audio_path)
#             notes = detect_notes(audio, sr)
#             output_simplified_score(notes, output_path_notes)
#             print("乐谱输出完成！")
#         except Exception as e:
#             print(f"乐谱识别失败: {e}")
#
#         try:
#             # 打开输出文件
#             webbrowser.open(output_path_notes)
#         except Exception as e:
#             print(f"打开输出文件失败: {e}")
#
#     def task_finished(self, task_name):
#         """任务完成后的回调函数"""
#         print(f"{task_name} 任务完成！")
#         self.enable_buttons()
#
#
# # 主函数入口
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()  # 显示窗口
#     sys.exit(app.exec_())  # 进入应用的事件循环


