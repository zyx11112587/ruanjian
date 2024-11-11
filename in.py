import os
import subprocess
import sys
import webbrowser  # 用于打开文件
import notation
import Shazam
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QThread, pyqtSignal
from ruanjian.get_notes import detect_notes, output_simplified_score
from ruanjian.load import load_audio
from ruanjian.recognition import recognize_with_timestamps
from ruanjian.transform import convert_audio
from ruanjian.new_ui import Ui_MainWidgt
from PyQt5.QtCore import QTimer

#鉴别输入路径的对错
def is_wav_file(file_path):
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        return False

    # 检查文件扩展名是否为 .wav
    return file_path.lower().endswith('.wav')

#耗时任务通过多线程来执行
class WorkerThread(QThread):
    # 定义完成操作后的信号
    finished = pyqtSignal(str)
    errored = pyqtSignal(str)

    def __init__(self, task, *args):
        super().__init__()
        self.task = task
        self.args = args

    def run(self):
        try:
            # 执行传入的任务函数
            result=self.task(*self.args)
            self.finished.emit(result)
        except Exception as e:
            self.errored.emit(self.task.__name__)


class MainWindow(QDialog, Ui_MainWidgt):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.disable_buttons()
        self.pushButton_0.setEnabled(True)
        self.input_edit.setReadOnly(True)
        # 为按钮添加点击事件
        self.pushButton_0.clicked.connect(self.pushButton_0_clicked)
        self.pushButton_1.clicked.connect(self.pushButton_1_clicked)
        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.pushButton_3.clicked.connect(self.pushButton_3_clicked)
        self.pushButton_4.clicked.connect(self.pushButton_4_clicked)
        self.CancelButton.clicked.connect(self.close)
        #所有线程对象提前初始化，防止因为生命周期产生的错误
        self.pushButton_1_worker = WorkerThread(self.separate_audio, r"fuck")
        self.pushButton_1_worker.finished.connect(self.pushButton_1_finished)
        self.pushButton_1_worker.errored.connect(self.pushButton_1_errored)

        self.pushButton_2_worker = WorkerThread(self.notation, r"fuck")
        self.pushButton_2_worker.finished.connect(self.pushButton_2_finished)
        self.pushButton_2_worker.errored.connect(self.pushButton_2_errored)

        self.pushButton_3_worker = WorkerThread(self.output_lyrics, r"fuck",r"fuck")
        self.pushButton_3_worker.finished.connect(self.pushButton_3_finished)
        self.pushButton_3_worker.errored.connect(self.pushButton_3_errored)

        self.pushButton_4_worker = WorkerThread(self.recognize_song, r"fuck")
        self.pushButton_4_worker.finished.connect(self.pushButton_4_finished)
        self.pushButton_4_worker.errored.connect(self.pushButton_4_errored)

        self.input_edit.returnPressed.connect(self.end_input)

    def disable_buttons(self):
        # """禁用所有按钮"""
        self.pushButton_0.setEnabled(False)
        self.pushButton_1.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        # """清空所有文本"""
        # self.input_file_label.clear()
        # self.label_0.setText("")
        # self.label_1.setText("")
        # self.label_2.setText("")
        # self.label_3.setText("")
        # self.textEdit.clear()
        # self.input_file_label.clear()


    def pushButton_0_clicked(self):
        print(1)
        self.disable_buttons()
        self.input_edit.setReadOnly(False)
        self.input_file_label.setText(r"请输入文件路径")

    def end_input(self):
        #不延迟启用该按钮的话会造成在启用的同时相应点击的槽函数
        QTimer.singleShot(100, lambda: self.pushButton_0.setEnabled(True))
        self.input_edit.setReadOnly(True)
        input_string = self.input_edit.text()
        if is_wav_file(input_string):
            self.input_file_label.setText(r"文件路径可用")
            self.pushButton_1.setEnabled(True)
        else:
            self.input_file_label.setText(r"文件路径不可用")

    #响应按钮1的点击
    def pushButton_1_clicked(self):
        input_string = self.input_edit.text()
        self.pushButton_1_worker.args= (input_string,)
        self.label_0.setText(r"分离音频中...请稍等")
        self.pushButton_1_worker.start()
        self.disable_buttons()
        self.textEdit.clear()

    def separate_audio(self, input_audio_path):
        try:
            subprocess.run(['demucs', input_audio_path], check=True)
            print(1)
            return "Succeed"
        except subprocess.CalledProcessError as e:
            return f"音频分离失败: {e}"
        except Exception as e:
            return f"音频分离发生未知错误: {e}"

    def pushButton_1_finished(self,result):
        print(2)
        if result == "Succeed":
            self.label_0.setText(r"分离音频成功！")
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
        else :
            self.textEdit.setPlainText(result)
            self.label_0.setText(r"分离音频失败！")

    def pushButton_1_errored(self,name):
        self.textEdit.setText(f"唤起进程失败：{name}")

    #相应按钮2的点击
    def pushButton_2_clicked(self):
        input_string = self.input_edit.text()
        self.pushButton_2_worker.args= (input_string,)
        self.label_1.setText(r"输出乐谱中...请稍等")
        self.pushButton_2_worker.start()
        self.disable_buttons()
        self.textEdit.clear()

    def notation(self, audio_file):
        try:
            notes = notation.extract_notes(audio_file, sample_interval=20)
            notation.plot_notes(notes, notes_per_line=60, output_file=r"wav/score2.png", staff_spacing=1)
            return "Succeed"
        except subprocess.CalledProcessError as e:
            return f"输出乐谱失败: {e}"
        except Exception as e:
            return f"输出乐谱发生未知错误: {e}"

    def pushButton_2_finished(self,result):
        if result == "Succeed":
            self.label_1.setText(r"输出乐谱成功！")
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
        else :
            self.textEdit.setText(result)
            self.label_1.setText(r"输出乐谱失败！")
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)

    def pushButton_2_errored(self,name):
        self.textEdit.setText(f"唤起进程失败：{name}")

    def pushButton_3_clicked(self):
        input_path = r"separated\htdemucs\music_1\vocals.wav"
        output_path = r"separated\htdemucs\music_1\vocals_1.wav"
        self.pushButton_3_worker.args= (input_path,output_path,)
        self.label_2.setText(r"输出歌词中...请稍等")
        self.pushButton_3_worker.start()
        self.disable_buttons()
        self.textEdit.clear()

    def output_lyrics(self, input_path, output_path):
        """歌词识别任务"""
        try:
            convert_audio(input_path, output_path)
            model_path = r"wav\vosk-model-cn-0.22"
            output_file_path = r"wav\output_1.txt"
            recognize_with_timestamps(output_path, model_path, output_file_path)
            with open(output_file_path, 'r', encoding='utf-8') as file:
                content = file.read() # 读取文件内容并存储 return content
                return content
        except Exception as e:
            return f"歌词识别失败"


    def pushButton_3_finished(self,result):
        if result == f"歌词识别失败":
            self.label_2.setText(r"输出歌词失败！")
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
        else :
            self.textEdit.setText(result)
            self.label_2.setText(r"输出歌词成功！")
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)

    def pushButton_3_errored(self,name):
        self.textEdit.setText(f"唤起进程失败：{name}")

    def pushButton_4_clicked(self):
        input_string = self.input_edit.text()
        self.pushButton_4_worker.args= (input_string,)
        self.label_3.setText(r"输出歌名中...请稍等")
        self.pushButton_4_worker.start()
        self.disable_buttons()
        self.textEdit.clear()

    def recognize_song(self, song_path):
        try:
            Shazam.recognize_song_info(song_path)
            return "Succeed"
        except subprocess.CalledProcessError as e:
            return f"输出歌名失败: {e}"
        except Exception as e:
            return f"输出歌名发生未知错误: {e}"

    def pushButton_4_finished(self,result):
        self.textEdit.setText(result)
        self.label_3.setText(r"输出歌名成功！")
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)

    def pushButton_4_errored(self,name):
        self.textEdit.setText(f"唤起进程失败：{name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



