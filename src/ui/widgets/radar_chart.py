"""
五维雷达图组件 - 可视化展示玩家属性
"""

import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPointF, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF, QPainterPath


class RadarChart(QWidget):
    """五维雷达图组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 300)

        # 属性数据
        self._attributes = {
            'knowledge': 0,
            'expression': 0,
            'empathy': 0,
            'perseverance': 0,
            'courage': 0
        }

        # 属性标签（中文）
        self.attr_labels = {
            'knowledge': '知识',
            'expression': '表达',
            'empathy': '共情',
            'perseverance': '毅力',
            'courage': '勇气'
        }

        # 动画相关
        self._animation_progress = 1.0
        self._target_attributes = self._attributes.copy()

        # 颜色配置
        self.grid_color = QColor(200, 200, 200)
        self.data_color = QColor(76, 175, 80, 150)  # 半透明绿色
        self.data_border_color = QColor(76, 175, 80)
        self.label_color = QColor(60, 60, 60)

    def set_attributes(self, attributes: dict, animated: bool = True):
        """
        设置属性值

        Args:
            attributes: 属性字典，键为属性名，值为属性值（0-100）
            animated: 是否使用动画
        """
        self._target_attributes = attributes.copy()

        if animated:
            # 使用动画过渡
            self.animate_to_target()
        else:
            # 直接设置
            self._attributes = attributes.copy()
            self.update()

    def animate_to_target(self):
        """动画过渡到目标值"""
        # 保存起始值
        self._start_attributes = self._attributes.copy()

        # 创建动画
        self.animation = QPropertyAnimation(self, b"animation_progress")
        self.animation.setDuration(800)  # 800ms
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.valueChanged.connect(self.on_animation_update)
        self.animation.start()

    def on_animation_update(self):
        """动画更新回调"""
        # 插值计算当前属性值
        progress = self._animation_progress
        for key in self._attributes.keys():
            start_val = self._start_attributes.get(key, 0)
            target_val = self._target_attributes.get(key, 0)
            self._attributes[key] = start_val + (target_val - start_val) * progress

        self.update()

    @pyqtProperty(float)
    def animation_progress(self):
        return self._animation_progress

    @animation_progress.setter
    def animation_progress(self, value):
        self._animation_progress = value

    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 计算绘图区域
        width = self.width()
        height = self.height()
        size = min(width, height)
        center_x = width / 2
        center_y = height / 2
        radius = size * 0.35  # 雷达图半径

        # 绘制网格
        self.draw_grid(painter, center_x, center_y, radius)

        # 绘制数据
        self.draw_data(painter, center_x, center_y, radius)

        # 绘制标签
        self.draw_labels(painter, center_x, center_y, radius)

    def draw_grid(self, painter: QPainter, cx: float, cy: float, radius: float):
        """绘制背景网格"""
        painter.setPen(QPen(self.grid_color, 1))

        # 绘制5个同心五边形（从内到外，每个代表20%）
        for level in range(1, 6):
            r = radius * (level / 5)
            polygon = self.create_pentagon(cx, cy, r)
            painter.drawPolygon(polygon)

        # 绘制从中心到顶点的连线
        for i in range(5):
            angle = self.get_angle(i)
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            painter.drawLine(int(cx), int(cy), int(x), int(y))

    def draw_data(self, painter: QPainter, cx: float, cy: float, radius: float):
        """绘制数据多边形"""
        # 创建数据多边形
        points = []
        for i, (key, label) in enumerate(self.attr_labels.items()):
            value = self._attributes.get(key, 0)
            # 将属性值映射到半径（假设最大值为100）
            ratio = min(value / 100.0, 1.0)
            angle = self.get_angle(i)
            x = cx + radius * ratio * math.cos(angle)
            y = cy + radius * ratio * math.sin(angle)
            points.append(QPointF(x, y))

        polygon = QPolygonF(points)

        # 填充数据区域
        painter.setBrush(QBrush(self.data_color))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(polygon)

        # 绘制数据边框
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(self.data_border_color, 2))
        painter.drawPolygon(polygon)

        # 绘制顶点
        painter.setBrush(QBrush(self.data_border_color))
        for point in points:
            painter.drawEllipse(point, 4, 4)

    def draw_labels(self, painter: QPainter, cx: float, cy: float, radius: float):
        """绘制属性标签"""
        painter.setPen(QPen(self.label_color))
        font = painter.font()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)

        label_offset = 30  # 标签距离雷达图的偏移

        for i, (key, label) in enumerate(self.attr_labels.items()):
            angle = self.get_angle(i)
            # 标签位置比雷达图外围更远
            x = cx + (radius + label_offset) * math.cos(angle)
            y = cy + (radius + label_offset) * math.sin(angle)

            # 获取属性值
            value = int(self._attributes.get(key, 0))
            text = f"{label}\n{value}"

            # 绘制文本（居中对齐）
            metrics = painter.fontMetrics()
            lines = text.split('\n')
            total_height = metrics.height() * len(lines)

            for j, line in enumerate(lines):
                text_width = metrics.horizontalAdvance(line)
                text_x = x - text_width / 2
                text_y = y - total_height / 2 + metrics.height() * (j + 1)
                painter.drawText(int(text_x), int(text_y), line)

    def create_pentagon(self, cx: float, cy: float, radius: float) -> QPolygonF:
        """创建正五边形"""
        points = []
        for i in range(5):
            angle = self.get_angle(i)
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append(QPointF(x, y))
        return QPolygonF(points)

    def get_angle(self, index: int) -> float:
        """
        获取第 i 个顶点的角度（从正上方开始，顺时针）

        Args:
            index: 顶点索引（0-4）

        Returns:
            float: 角度（弧度）
        """
        # 从正上方开始（-90度），顺时针旋转
        # 五边形每个角相隔 72度 (360/5)
        base_angle = -math.pi / 2  # -90度（正上方）
        return base_angle + (2 * math.pi / 5) * index


# 测试代码
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton

    app = QApplication(sys.argv)

    # 创建窗口
    window = QWidget()
    window.setWindowTitle("五维雷达图测试")
    window.setGeometry(100, 100, 500, 600)

    layout = QVBoxLayout(window)

    # 创建雷达图
    chart = RadarChart()
    layout.addWidget(chart)

    # 初始数据
    chart.set_attributes({
        'knowledge': 60,
        'expression': 40,
        'empathy': 50,
        'perseverance': 70,
        'courage': 30
    }, animated=False)

    # 测试按钮：动画更新数据
    def update_data():
        import random
        chart.set_attributes({
            'knowledge': random.randint(20, 100),
            'expression': random.randint(20, 100),
            'empathy': random.randint(20, 100),
            'perseverance': random.randint(20, 100),
            'courage': random.randint(20, 100)
        }, animated=True)

    btn = QPushButton("随机更新数据（动画）")
    btn.clicked.connect(update_data)
    layout.addWidget(btn)

    window.show()
    sys.exit(app.exec_())
