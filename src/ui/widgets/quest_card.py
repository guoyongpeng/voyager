"""
任务卡片组件 - 显示单个任务的信息
"""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMenu, QAction
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QCursor


class QuestCard(QFrame):
    """任务卡片组件"""

    # 信号
    quest_clicked = pyqtSignal(int)  # 任务点击（任务ID）
    quest_started = pyqtSignal(int)  # 开始任务
    quest_completed = pyqtSignal(int)  # 完成任务
    quest_abandoned = pyqtSignal(int)  # 放弃任务

    def __init__(self, quest_data: dict, parent=None):
        """
        初始化任务卡片

        Args:
            quest_data: 任务数据字典
            parent: 父组件
        """
        super().__init__(parent)
        self.quest_data = quest_data
        self.quest_id = quest_data['id']

        self.init_ui()
        self.setup_animations()

    def init_ui(self):
        """初始化 UI"""
        self.setFrameShape(QFrame.StyledPanel)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # 根据状态设置样式
        self.update_style()

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 12, 15, 12)
        main_layout.setSpacing(8)

        # 顶部：标题 + 类型标签
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        # 任务标题
        self.title_label = QLabel(self.quest_data['title'])
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)
        header_layout.addWidget(self.title_label, 1)

        # 类型标签
        quest_type = self.quest_data.get('type', 'side')
        type_labels = {
            'main': '主线',
            'side': '支线',
            'daily': '每日'
        }
        type_colors = {
            'main': '#FF9800',
            'side': '#2196F3',
            'daily': '#9C27B0'
        }

        type_label = QLabel(type_labels.get(quest_type, '支线'))
        type_label.setStyleSheet(f"""
            background-color: {type_colors.get(quest_type, '#2196F3')};
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
        """)
        type_label.setFixedHeight(22)
        header_layout.addWidget(type_label)

        main_layout.addLayout(header_layout)

        # 任务描述
        description = self.quest_data.get('description', '')
        if description:
            desc_label = QLabel(description)
            desc_label.setStyleSheet("color: #666; font-size: 12px;")
            desc_label.setWordWrap(True)
            desc_label.setMaximumHeight(40)
            main_layout.addWidget(desc_label)

        # 底部：状态 + 操作按钮
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 5, 0, 0)

        # 状态标签
        status = self.quest_data.get('status', 'pending')
        status_labels = {
            'pending': '待开始',
            'in_progress': '进行中',
            'completed': '已完成',
            'abandoned': '已放弃'
        }
        status_colors = {
            'pending': '#757575',
            'in_progress': '#4CAF50',
            'completed': '#2196F3',
            'abandoned': '#F44336'
        }

        self.status_label = QLabel(f"● {status_labels.get(status, '未知')}")
        self.status_label.setStyleSheet(f"""
            color: {status_colors.get(status, '#757575')};
            font-size: 12px;
            font-weight: bold;
        """)
        footer_layout.addWidget(self.status_label)

        footer_layout.addStretch()

        # 更多操作按钮
        more_btn = QPushButton("⋮")
        more_btn.setFixedSize(24, 24)
        more_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 18px;
                color: #999;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border-radius: 12px;
            }
        """)
        more_btn.clicked.connect(self.show_context_menu)
        footer_layout.addWidget(more_btn)

        main_layout.addLayout(footer_layout)

    def update_style(self):
        """根据状态更新样式"""
        status = self.quest_data.get('status', 'pending')

        base_style = """
            QuestCard {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
            }
            QuestCard:hover {
                border-color: #4CAF50;
                background-color: #f9f9f9;
            }
        """

        # 已完成的任务半透明
        if status == 'completed':
            base_style += """
                QuestCard {
                    opacity: 0.7;
                }
            """
        elif status == 'abandoned':
            base_style += """
                QuestCard {
                    opacity: 0.5;
                    border-color: #ffcdd2;
                }
            """

        self.setStyleSheet(base_style)

    def setup_animations(self):
        """设置动画效果"""
        # 创建悬停动画（可选，暂时省略）
        pass

    def show_context_menu(self):
        """显示右键菜单"""
        menu = QMenu(self)
        status = self.quest_data.get('status', 'pending')

        # 根据状态显示不同选项
        if status == 'pending':
            start_action = QAction("开始任务", self)
            start_action.triggered.connect(lambda: self.quest_started.emit(self.quest_id))
            menu.addAction(start_action)

        elif status == 'in_progress':
            complete_action = QAction("完成任务", self)
            complete_action.triggered.connect(lambda: self.quest_completed.emit(self.quest_id))
            menu.addAction(complete_action)

        if status in ['pending', 'in_progress']:
            menu.addSeparator()
            abandon_action = QAction("放弃任务", self)
            abandon_action.triggered.connect(lambda: self.quest_abandoned.emit(self.quest_id))
            menu.addAction(abandon_action)

        # 查看详情
        menu.addSeparator()
        detail_action = QAction("查看详情", self)
        detail_action.triggered.connect(lambda: self.quest_clicked.emit(self.quest_id))
        menu.addAction(detail_action)

        # 显示菜单
        menu.exec_(QCursor.pos())

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.quest_clicked.emit(self.quest_id)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """鼠标进入事件"""
        # 可以添加悬停效果
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开事件"""
        super().leaveEvent(event)


# 测试代码
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("任务卡片测试")
    window.setGeometry(100, 100, 400, 600)

    layout = QVBoxLayout(window)
    layout.setSpacing(10)

    # 测试数据
    test_quests = [
        {
            'id': 1,
            'title': '学习 Python 装饰器',
            'description': '深入理解装饰器的原理和使用场景',
            'type': 'main',
            'status': 'in_progress'
        },
        {
            'id': 2,
            'title': '阅读《代码整洁之道》第3章',
            'description': '学习如何编写整洁的函数',
            'type': 'side',
            'status': 'pending'
        },
        {
            'id': 3,
            'title': '完成每日代码练习',
            'description': '',
            'type': 'daily',
            'status': 'completed'
        },
        {
            'id': 4,
            'title': '学习 React Hooks',
            'description': '理解 useState 和 useEffect',
            'type': 'side',
            'status': 'abandoned'
        }
    ]

    # 创建卡片
    for quest in test_quests:
        card = QuestCard(quest)
        card.quest_clicked.connect(lambda qid: print(f"点击任务 {qid}"))
        card.quest_started.connect(lambda qid: print(f"开始任务 {qid}"))
        card.quest_completed.connect(lambda qid: print(f"完成任务 {qid}"))
        layout.addWidget(card)

    layout.addStretch()

    window.show()
    sys.exit(app.exec_())
