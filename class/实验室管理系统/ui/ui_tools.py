from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtCore import QPoint

class UITools:
    @staticmethod
    def center_window(window: QWidget):
        """将窗口居中显示"""
        # 获取屏幕几何信息
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口几何信息
        window_size = window.geometry()
        
        # 计算居中位置
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        
        # 移动窗口
        window.move(x, y)
        
    @staticmethod
    def adjust_new_window_position(current_window: QWidget, new_window: QWidget, offset: tuple = (0, 0)):
        """
        根据当前窗口位置，调整新窗口的位置
        
        Args:
            current_window: 当前窗口
            new_window: 要调整位置的新窗口
            offset: (x, y) 相对于当前窗口的偏移量，默认为(30, 30)
        """
        # 获取当前窗口的位置
        current_pos = current_window.pos()
        
        # 计算新窗口的位置（添加一个小偏移，避免完全重叠）
        new_x = current_pos.x() + offset[0]
        new_y = current_pos.y() + offset[1]
        
        # 确保新窗口不会超出屏幕范围
        screen = QDesktopWidget().screenGeometry()
        new_x = min(max(0, new_x), screen.width() - new_window.width())
        new_y = min(max(0, new_y), screen.height() - new_window.height())
        
        # 移动新窗口到计算出的位置
        new_window.move(new_x, new_y)
    
    @staticmethod
    def save_window_position(window: QWidget) -> QPoint:
        """保存窗口位置"""
        return window.pos()
    
    @staticmethod
    def restore_window_position(window: QWidget, position: QPoint):
        """还原窗口位置"""
        if position:
            window.move(position)
    
    @staticmethod
    def ensure_window_visible(window: QWidget):
        """确保窗口在屏幕可见范围内"""
        screen = QDesktopWidget().screenGeometry()
        window_geo = window.geometry()
        
        # 如果窗口位置在屏幕外，将其移动到可见区域
        if window_geo.left() < 0:
            window_geo.moveLeft(0)
        if window_geo.top() < 0:
            window_geo.moveTop(0)
        if window_geo.right() > screen.width():
            window_geo.moveRight(screen.width())
        if window_geo.bottom() > screen.height():
            window_geo.moveBottom(screen.height())
            
        window.setGeometry(window_geo) 