import sys
import time
import queue
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue

    def run(self):
        while True:
            try:
                task = self.task_queue.get(block=False)
                self.update_signal.emit(f"处理任务: {task}")
                time.sleep(2)  # 模拟任务处理时间
                self.task_queue.task_done()
            except queue.Empty:
                break

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("多线程示例")
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel("等待开始...", self)
        self.button = QPushButton("添加任务", self)
        self.button.clicked.connect(self.add_task)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.task_queue = queue.Queue()
        self.thread = WorkerThread(self.task_queue)
        self.thread.update_signal.connect(self.update_label)

    def add_task(self):
        self.task_queue.put(f"任务 {self.task_queue.qsize() + 1}")
        if not self.thread.isRunning():
            self.thread.start()

    def update_label(self, text):
        self.label.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())