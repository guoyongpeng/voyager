"""
任务面板组件 - 管理和显示所有任务
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QButtonGroup,
    QRadioButton, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from .quest_card import QuestCard


class QuestPanel(QWidget):
    """任务面板组件"""

    # 信号
    quest_created = pyqtSignal()  # 创建新任务
    quest_detail_requested = pyqtSignal(int)  # 请求查看任务详情
    quest_status_changed = pyqtSignal()  # 任务状态改变

    def __init__(self, quest_manager, parent=None):
        """
        初始化任务面板

        Args:
            quest_manager: Quest 实例
            parent: 父组件
        """
        super().__init__(parent)
        self.quest_mgr = quest_manager
        self.current_filter = 'all'  # 当前筛选条件

        self.init_ui()
        self.load_quests()

    def init_ui(self):
        """初始化 UI"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 顶部栏：标题 + 新建按钮
        header = self.create_header()
        main_layout.addWidget(header)

        # 筛选栏
        filter_bar = self.create_filter_bar()
        main_layout.addWidget(filter_bar)

        # 任务列表区域（可滚动）
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)

        # 任务容器
        self.quest_container = QWidget()
        self.quest_layout = QVBoxLayout(self.quest_container)
        self.quest_layout.setSpacing(10)
        self.quest_layout.setContentsMargins(0, 0, 0, 0)
        self.quest_layout.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.quest_container)
        main_layout.addWidget(scroll_area)

    def create_header(self):
        """创建顶部栏"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        # 标题
        title = QLabel("任务列表")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        layout.addStretch()

        # 新建任务按钮
        new_btn = QPushButton("+ 新建任务")
        new_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        new_btn.clicked.connect(self.quest_created.emit)
        layout.addWidget(new_btn)

        return header

    def create_filter_bar(self):
        """创建筛选栏"""
        filter_bar = QWidget()
        layout = QHBoxLayout(filter_bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 筛选按钮组
        self.filter_group = QButtonGroup(self)

        filters = [
            ('all', '全部'),
            ('pending', '待开始'),
            ('in_progress', '进行中'),
            ('completed', '已完成')
        ]

        for filter_key, filter_name in filters:
            btn = QRadioButton(filter_name)
            btn.setStyleSheet("""
                QRadioButton {
                    font-size: 13px;
                    padding: 5px 10px;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
            """)
            btn.toggled.connect(lambda checked, key=filter_key: self.on_filter_changed(key) if checked else None)
            self.filter_group.addButton(btn)
            layout.addWidget(btn)

            # 默认选中"全部"
            if filter_key == 'all':
                btn.setChecked(True)

        layout.addStretch()

        return filter_bar

    def load_quests(self):
        """加载任务列表"""
        # 清空现有卡片
        self.clear_quest_cards()

        # 获取任务
        if self.current_filter == 'all':
            quests = self.quest_mgr.get_active_quests()
        else:
            quests = self.quest_mgr.get_active_quests(status=self.current_filter)

        # 如果没有任务，显示提示
        if not quests:
            empty_label = QLabel(self.get_empty_message())
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("""
                font-size: 14px;
                color: #999;
                padding: 40px;
            """)
            self.quest_layout.addWidget(empty_label)
            return

        # 按状态分组排序
        status_order = ['in_progress', 'pending', 'completed', 'abandoned']
        quests_sorted = sorted(quests, key=lambda q: (
            status_order.index(q['status']) if q['status'] in status_order else 999,
            -q['id']  # 按ID倒序（新的在前）
        ))

        # 创建卡片
        for quest in quests_sorted:
            card = QuestCard(quest)
            card.quest_clicked.connect(self.quest_detail_requested.emit)
            card.quest_started.connect(self.on_quest_started)
            card.quest_completed.connect(self.on_quest_completed)
            card.quest_abandoned.connect(self.on_quest_abandoned)
            self.quest_layout.addWidget(card)

    def clear_quest_cards(self):
        """清空所有任务卡片"""
        while self.quest_layout.count():
            item = self.quest_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def get_empty_message(self):
        """获取空状态提示信息"""
        messages = {
            'all': "暂无任务\n点击右上角「+ 新建任务」开始吧！",
            'pending': "没有待开始的任务",
            'in_progress': "没有进行中的任务",
            'completed': "还没有完成的任务\n加油！"
        }
        return messages.get(self.current_filter, "暂无任务")

    def on_filter_changed(self, filter_key: str):
        """筛选条件改变"""
        self.current_filter = filter_key
        self.load_quests()

    def on_quest_started(self, quest_id: int):
        """开始任务"""
        success = self.quest_mgr.start_quest(quest_id)
        if success:
            QMessageBox.information(self, "成功", "任务已开始！")
            self.quest_status_changed.emit()
            self.refresh()
        else:
            QMessageBox.warning(self, "失败", "无法开始此任务")

    def on_quest_completed(self, quest_id: int):
        """完成任务"""
        # 这里应该弹出心得输入对话框，暂时简化处理
        from PyQt5.QtWidgets import QInputDialog

        summary, ok = QInputDialog.getMultiLineText(
            self,
            "完成任务",
            "请分享你的心得体会：",
            ""
        )

        if ok and summary:
            # 简化：使用固定奖励
            result = self.quest_mgr.complete_quest(
                quest_id=quest_id,
                summary=summary,
                xp_awarded=50,
                attributes_awarded={'knowledge': 10},
                ai_feedback="很好！继续加油！"
            )

            if result['success']:
                QMessageBox.information(
                    self,
                    "任务完成",
                    f"恭喜完成任务！\n\n获得奖励：\n经验值: +50 XP\n知识: +10"
                )
                self.quest_status_changed.emit()
                self.refresh()
            else:
                QMessageBox.warning(self, "失败", result.get('error', '未知错误'))

    def on_quest_abandoned(self, quest_id: int):
        """放弃任务"""
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要放弃这个任务吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = self.quest_mgr.abandon_quest(quest_id)
            if success:
                QMessageBox.information(self, "已放弃", "任务已放弃")
                self.quest_status_changed.emit()
                self.refresh()
            else:
                QMessageBox.warning(self, "失败", "无法放弃此任务")

    def refresh(self):
        """刷新任务列表"""
        self.load_quests()


# 测试代码
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from ...database.db_manager import DatabaseManager
    from ...core.quest import Quest

    app = QApplication(sys.argv)

    # 创建测试数据
    db = DatabaseManager("data/voyager_test.db")
    quest_mgr = Quest(db, user_id=1)

    # 创建窗口
    panel = QuestPanel(quest_mgr)
    panel.setWindowTitle("任务面板测试")
    panel.setGeometry(100, 100, 800, 600)
    panel.show()

    sys.exit(app.exec_())
