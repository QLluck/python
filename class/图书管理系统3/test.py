import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # 创建滚动区域的内容 widget
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)

        # 创建内容 widget 的布局管理器
        self.content_layout = QVBoxLayout(self.content_widget)

        # 创建主窗口的布局管理器，并将滚动区域添加进去
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)

        # 创建一个按钮，用于动态增加布局
        self.add_layout_button = QPushButton("添加布局")
        self.add_layout_button.clicked.connect(self.add_layout)
        main_layout.addWidget(self.add_layout_button)

        # 初始化一个计数器，用于标识添加的布局
        self.layout_count = 0

    def add_layout(self):
        """动态添加布局到滚动区域"""
        # 先清空布局中的内容
        item_list = list(range(self._ui.myLayout.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self._ui.myLayout.itemAt(i)
            self._ui.myLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        # 创建一个新的水平布局
        new_layout = QHBoxLayout()

        # 添加一些控件到水平布局中
        label = QLabel(f"这是布局 {self.layout_count} 中的内容")
        new_layout.addWidget(label)

        # 将水平布局添加到内容 widget 的垂直布局中
        self.content_layout.addLayout(new_layout)

        # 计数器加 1
        self.layout_count += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())