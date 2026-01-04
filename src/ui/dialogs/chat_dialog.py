"""
对话窗口 - 与 AI 助手"凯"交互
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QScrollArea, QWidget,
    QLabel, QFrame
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor


class MessageBubble(QFrame):
    """消息气泡组件"""

    def __init__(self, text: str, is_user: bool = True, parent=None):
        """
        初始化消息气泡

        Args:
            text: 消息文本
            is_user: 是否为用户消息（True: 用户, False: AI）
            parent: 父组件
        """
        super().__init__(parent)
        self.text = text
        self.is_user = is_user

        self.init_ui()

    def init_ui(self):
        """初始化 UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # 根据发送者调整对齐方式
        if self.is_user:
            layout.addStretch()

        # 消息内容
        message_label = QLabel(self.text)
        message_label.setWordWrap(True)
        message_label.setMaximumWidth(400)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # 样式
        if self.is_user:
            # 用户消息：蓝色背景，右对齐
            message_label.setStyleSheet("""
                QLabel {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 15px;
                    border-radius: 15px;
                    font-size: 13px;
                }
            """)
        else:
            # AI 消息：灰色背景，左对齐
            message_label.setStyleSheet("""
                QLabel {
                    background-color: #f0f0f0;
                    color: #333;
                    padding: 10px 15px;
                    border-radius: 15px;
                    font-size: 13px;
                }
            """)

        layout.addWidget(message_label)

        if not self.is_user:
            layout.addStretch()


class ChatDialog(QDialog):
    """对话窗口"""

    # 信号
    message_sent = pyqtSignal(str)  # 发送消息信号

    def __init__(self, kai, parent=None):
        """
        初始化对话窗口

        Args:
            kai: Kai 实例（AI 助手）
            parent: 父窗口
        """
        super().__init__(parent)
        self.kai = kai

        self.setWindowTitle("与凯对话")
        self.setGeometry(200, 100, 500, 700)

        self.init_ui()

        # 显示欢迎消息
        self.show_welcome_message()

    def init_ui(self):
        """初始化 UI"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 标题栏
        header = self.create_header()
        main_layout.addWidget(header)

        # 消息区域（可滚动）
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: white;
                border: none;
            }
        """)

        # 消息容器
        self.message_container = QWidget()
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setSpacing(10)
        self.message_layout.setContentsMargins(10, 10, 10, 10)
        self.message_layout.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.message_container)
        self.scroll_area = scroll_area
        main_layout.addWidget(scroll_area)

        # 输入区域
        input_area = self.create_input_area()
        main_layout.addWidget(input_area)

    def create_header(self):
        """创建标题栏"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #4CAF50;
                padding: 15px;
            }
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 10, 15, 10)

        # 标题
        title = QLabel("AI 助手 · 凯")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: white;
        """)
        layout.addWidget(title)

        layout.addStretch()

        # 状态标签
        status = QLabel("● 在线")
        status.setStyleSheet("""
            font-size: 12px;
            color: white;
        """)
        layout.addWidget(status)

        return header

    def create_input_area(self):
        """创建输入区域"""
        input_area = QFrame()
        input_area.setStyleSheet("""
            QFrame {
                background-color: #f8f8f8;
                border-top: 1px solid #ddd;
            }
        """)

        layout = QHBoxLayout(input_area)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)

        # 输入框
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入消息...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 20px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_field, 1)

        # 发送按钮
        send_btn = QPushButton("发送")
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        send_btn.clicked.connect(self.send_message)
        layout.addWidget(send_btn)

        return input_area

    def show_welcome_message(self):
        """显示欢迎消息"""
        welcome = "你好！我是凯，你的AI成长助手。\n\n我可以帮你：\n• 拆解任务目标\n• 提供执行建议\n• 评判完成情况\n• 关心你的状态\n\n有什么我可以帮助的吗？"
        self.add_message(welcome, is_user=False)

    def add_message(self, text: str, is_user: bool):
        """
        添加消息到对话框

        Args:
            text: 消息文本
            is_user: 是否为用户消息
        """
        bubble = MessageBubble(text, is_user)
        self.message_layout.addWidget(bubble)

        # 自动滚动到底部
        QTimer.singleShot(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def send_message(self):
        """发送消息"""
        text = self.input_field.text().strip()
        if not text:
            return

        # 添加用户消息
        self.add_message(text, is_user=True)

        # 清空输入框
        self.input_field.clear()

        # 生成 AI 回复
        self.generate_ai_response(text)

        # 发送信号
        self.message_sent.emit(text)

    def generate_ai_response(self, user_message: str):
        """
        生成 AI 回复

        Args:
            user_message: 用户消息
        """
        # 简单的关键词响应（可以后续集成更复杂的逻辑）
        response = ""

        # 问候
        if any(word in user_message for word in ['你好', '嗨', 'hi', 'hello']):
            response = "你好！很高兴见到你！有什么我可以帮助的吗？"

        # 情绪检测
        elif any(word in user_message for word in ['累', '疲惫', '压力', '焦虑']):
            emotion_result = self.kai.analyze_emotion(user_message)
            if emotion_result:
                response = emotion_result.get('suggestion', '要注意休息哦~')
            else:
                response = "听起来你有些疲惫，要不要休息一下？"

        # 任务相关
        elif '任务' in user_message or '目标' in user_message:
            if '拆解' in user_message or '怎么做' in user_message:
                response = "我可以帮你拆解任务！请告诉我你的目标是什么？"
            else:
                response = "关于任务管理，我可以帮你拆解目标、提供建议。你具体想了解什么呢？"

        # 帮助
        elif '帮助' in user_message or '功能' in user_message or '能做' in user_message:
            response = "我的主要功能包括：\n\n1. 任务拆解 - 把大目标分解为小任务\n2. 执行建议 - 提供任务执行的具体建议\n3. 奖励评判 - 根据你的心得评估奖励\n4. 情绪关怀 - 检测你的状态并主动关心\n\n试试告诉我你的目标吧！"

        # 默认回复
        else:
            import random
            default_responses = [
                "我明白了，继续说吧~",
                "有意思，然后呢？",
                "嗯嗯，我在听~",
                "说得很好！",
                "继续加油！"
            ]
            response = random.choice(default_responses)

        # 添加 AI 回复
        self.add_message(response, is_user=False)

    def closeEvent(self, event):
        """关闭事件"""
        # 可以在这里保存对话历史
        event.accept()


# 测试代码
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from ...ai.kai import Kai

    app = QApplication(sys.argv)

    # 创建 AI 助手
    kai = Kai(config_manager=None)

    # 创建对话窗口
    dialog = ChatDialog(kai)
    dialog.show()

    sys.exit(app.exec_())
