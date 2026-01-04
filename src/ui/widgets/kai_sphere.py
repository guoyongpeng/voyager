"""
凯悬浮球组件 - AI 助手的可视化入口
"""

from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    pyqtSignal, pyqtProperty, QPoint
)
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont


class KaiSphere(QWidget):
    """凯悬浮球组件"""

    # 信号
    clicked = pyqtSignal()  # 点击信号

    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置固定大小
        self.sphere_size = 60
        self.setFixedSize(self.sphere_size, self.sphere_size)

        # 动画属性
        self._opacity = 1.0
        self._scale = 1.0

        # 设置样式
        self.setCursor(Qt.PointingHandCursor)

        # 设置窗口属性（无边框、置顶）
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 启动呼吸动画
        self.setup_breathing_animation()

    def setup_breathing_animation(self):
        """设置呼吸动画"""
        # 不透明度动画
        self.opacity_animation = QPropertyAnimation(self, b"opacity")
        self.opacity_animation.setDuration(2000)  # 2秒
        self.opacity_animation.setStartValue(0.6)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutSine)
        self.opacity_animation.setLoopCount(-1)  # 无限循环

        # 缩放动画
        self.scale_animation = QPropertyAnimation(self, b"scale")
        self.scale_animation.setDuration(2000)  # 2秒
        self.scale_animation.setStartValue(0.95)
        self.scale_animation.setEndValue(1.05)
        self.scale_animation.setEasingCurve(QEasingCurve.InOutSine)
        self.scale_animation.setLoopCount(-1)  # 无限循环

        # 启动动画
        self.opacity_animation.start()
        self.scale_animation.start()

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()

    @pyqtProperty(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.update()

    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 计算中心和半径
        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = (self.sphere_size / 2 - 5) * self._scale

        # 绘制外圈光晕（半透明）
        glow_color = QColor(76, 175, 80, int(50 * self._opacity))
        painter.setBrush(QBrush(glow_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            int(center_x - radius - 5),
            int(center_y - radius - 5),
            int((radius + 5) * 2),
            int((radius + 5) * 2)
        )

        # 绘制主圆球
        main_color = QColor(76, 175, 80, int(255 * self._opacity))
        painter.setBrush(QBrush(main_color))
        painter.setPen(QPen(QColor(255, 255, 255, int(200 * self._opacity)), 2))
        painter.drawEllipse(
            int(center_x - radius),
            int(center_y - radius),
            int(radius * 2),
            int(radius * 2)
        )

        # 绘制文字 "凯"
        painter.setPen(QColor(255, 255, 255, int(255 * self._opacity)))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, "凯")

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """鼠标进入事件 - 暂停动画"""
        self.opacity_animation.pause()
        self.scale_animation.pause()
        self._opacity = 1.0
        self._scale = 1.1
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开事件 - 恢复动画"""
        self.opacity_animation.resume()
        self.scale_animation.resume()
        super().leaveEvent(event)


# 测试代码
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

    app = QApplication(sys.argv)

    # 创建主窗口
    window = QMainWindow()
    window.setWindowTitle("凯悬浮球测试")
    window.setGeometry(100, 100, 800, 600)

    # 创建背景
    label = QLabel("点击右下角的凯悬浮球", window)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("font-size: 24px; color: #666;")
    window.setCentralWidget(label)

    # 创建凯悬浮球
    kai_sphere = KaiSphere(window)
    kai_sphere.clicked.connect(lambda: print("凯被点击了！"))

    # 定位到右下角
    def position_sphere():
        x = window.width() - kai_sphere.width() - 30
        y = window.height() - kai_sphere.height() - 30
        kai_sphere.move(x, y)

    # 窗口大小改变时重新定位
    def on_resize(event):
        position_sphere()
        return super(QMainWindow, window).resizeEvent(event)

    window.resizeEvent = on_resize
    position_sphere()

    window.show()
    sys.exit(app.exec_())
