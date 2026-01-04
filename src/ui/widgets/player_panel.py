"""
玩家面板组件 - 显示等级、经验、属性等信息
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QProgressBar, QFrame, QPushButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from .radar_chart import RadarChart


class PlayerPanel(QWidget):
    """玩家面板组件"""

    # 信号
    level_up = pyqtSignal(int)  # 升级信号（新等级）

    def __init__(self, player, parent=None):
        """
        初始化玩家面板

        Args:
            player: Player 实例
            parent: 父组件
        """
        super().__init__(parent)
        self.player = player

        self.init_ui()
        self.load_data()

    def init_ui(self):
        """初始化 UI"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: "Microsoft YaHei", "SimHei", sans-serif;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 标题
        title = QLabel("玩家信息")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #333;
            padding-bottom: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #ddd;")
        main_layout.addWidget(line)

        # 等级信息
        level_section = self.create_level_section()
        main_layout.addWidget(level_section)

        # 经验条
        xp_section = self.create_xp_section()
        main_layout.addWidget(xp_section)

        # 五维雷达图
        self.radar_chart = RadarChart()
        self.radar_chart.setMinimumHeight(280)
        main_layout.addWidget(self.radar_chart)

        # 属性统计
        attrs_section = self.create_attributes_section()
        main_layout.addWidget(attrs_section)

        # 底部弹性空间
        main_layout.addStretch()

    def create_level_section(self):
        """创建等级信息区域"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 等级标签
        level_label = QLabel("等级")
        level_label.setStyleSheet("font-size: 14px; color: #666;")
        layout.addWidget(level_label)

        layout.addStretch()

        # 等级值
        self.level_value = QLabel(f"Lv.{self.player.level}")
        self.level_value.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
        """)
        layout.addWidget(self.level_value)

        return widget

    def create_xp_section(self):
        """创建经验条区域"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # 经验数值标签
        xp_label_layout = QHBoxLayout()
        xp_label_layout.setContentsMargins(0, 0, 0, 0)

        self.xp_label = QLabel()
        self.xp_label.setStyleSheet("font-size: 12px; color: #666;")
        xp_label_layout.addWidget(self.xp_label)

        xp_label_layout.addStretch()

        self.xp_percent_label = QLabel()
        self.xp_percent_label.setStyleSheet("font-size: 12px; color: #666;")
        xp_label_layout.addWidget(self.xp_percent_label)

        layout.addLayout(xp_label_layout)

        # 经验进度条
        self.xp_progress = QProgressBar()
        self.xp_progress.setTextVisible(False)
        self.xp_progress.setFixedHeight(20)
        self.xp_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 10px;
                background-color: white;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 9px;
            }
        """)
        layout.addWidget(self.xp_progress)

        return widget

    def create_attributes_section(self):
        """创建属性统计区域"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(8)

        # 总属性点
        total_layout = QHBoxLayout()
        total_layout.setContentsMargins(0, 0, 0, 0)

        total_label = QLabel("总属性点")
        total_label.setStyleSheet("font-size: 13px; color: #666;")
        total_layout.addWidget(total_label)

        total_layout.addStretch()

        self.total_attr_value = QLabel()
        self.total_attr_value.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #4CAF50;
        """)
        total_layout.addWidget(self.total_attr_value)

        layout.addLayout(total_layout)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #ddd;")
        layout.addWidget(line)

        # 各项属性
        self.attr_labels = {}
        attr_names = {
            'knowledge': '知识',
            'expression': '表达',
            'empathy': '共情',
            'perseverance': '毅力',
            'courage': '勇气'
        }

        for key, name in attr_names.items():
            attr_layout = QHBoxLayout()
            attr_layout.setContentsMargins(0, 0, 0, 0)

            name_label = QLabel(name)
            name_label.setStyleSheet("font-size: 13px; color: #666;")
            attr_layout.addWidget(name_label)

            attr_layout.addStretch()

            value_label = QLabel()
            value_label.setStyleSheet("font-size: 13px; color: #333; font-weight: bold;")
            self.attr_labels[key] = value_label
            attr_layout.addWidget(value_label)

            layout.addLayout(attr_layout)

        return widget

    def load_data(self):
        """加载玩家数据"""
        # 更新等级
        self.level_value.setText(f"Lv.{self.player.level}")

        # 更新经验条
        current_xp = self.player.current_xp
        xp_for_next = self.player.calculate_xp_for_level(self.player.level + 1)
        xp_progress = self.player.get_progress_to_next_level()

        self.xp_label.setText(f"经验: {current_xp} / {xp_for_next} XP")
        self.xp_percent_label.setText(f"{int(xp_progress * 100)}%")
        self.xp_progress.setMaximum(100)
        self.xp_progress.setValue(int(xp_progress * 100))

        # 更新属性
        attributes = self.player.get_attributes()
        for key, label in self.attr_labels.items():
            value = attributes.get(key, 0)
            label.setText(str(value))

        # 更新总属性点
        total = self.player.get_total_attribute_points()
        self.total_attr_value.setText(str(total))

        # 更新雷达图
        self.radar_chart.set_attributes(attributes, animated=False)

    def refresh(self):
        """刷新数据（从数据库重新加载）"""
        old_level = self.player.level
        self.player.refresh()
        new_level = self.player.level

        # 检查是否升级
        if new_level > old_level:
            self.level_up.emit(new_level)

        # 重新加载数据（使用动画）
        self.load_data_animated()

    def load_data_animated(self):
        """加载玩家数据（使用动画）"""
        # 更新等级
        self.level_value.setText(f"Lv.{self.player.level}")

        # 更新经验条
        current_xp = self.player.current_xp
        xp_for_next = self.player.calculate_xp_for_level(self.player.level + 1)
        xp_progress = self.player.get_progress_to_next_level()

        self.xp_label.setText(f"经验: {current_xp} / {xp_for_next} XP")
        self.xp_percent_label.setText(f"{int(xp_progress * 100)}%")
        self.xp_progress.setValue(int(xp_progress * 100))

        # 更新属性
        attributes = self.player.get_attributes()
        for key, label in self.attr_labels.items():
            value = attributes.get(key, 0)
            label.setText(str(value))

        # 更新总属性点
        total = self.player.get_total_attribute_points()
        self.total_attr_value.setText(str(total))

        # 更新雷达图（带动画）
        self.radar_chart.set_attributes(attributes, animated=True)


# 测试代码
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from ...database.db_manager import DatabaseManager
    from ...core.player import Player

    app = QApplication(sys.argv)

    # 创建测试数据
    db = DatabaseManager("data/voyager_test.db")
    player = Player(db, user_id=1)

    # 创建窗口
    panel = PlayerPanel(player)
    panel.setWindowTitle("玩家面板测试")
    panel.setFixedWidth(350)
    panel.setMinimumHeight(700)
    panel.show()

    sys.exit(app.exec_())
