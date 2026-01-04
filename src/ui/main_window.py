"""
主窗口 - 应用的主界面
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QAction, QMessageBox, QMenuBar, QStatusBar
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

from ..database.db_manager import DatabaseManager
from ..core.player import Player
from ..core.quest import Quest
from ..ai.kai import Kai
from ..config import ConfigManager
from .widgets.player_panel import PlayerPanel
from .widgets.quest_panel import QuestPanel
from .widgets.kai_sphere import KaiSphere
from .dialogs.chat_dialog import ChatDialog


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("启航者 (Voyager) - 个人成长游戏化助手")
        self.setGeometry(100, 100, 1200, 800)

        # 初始化核心组件
        self.init_core_components()

        # 创建 UI
        self.init_ui()

        # 加载数据
        self.load_data()

    def init_core_components(self):
        """初始化核心组件"""
        # 配置管理器
        self.config = ConfigManager()

        # 数据库管理器
        db_path = "data/voyager.db"
        self.db = DatabaseManager(db_path)

        # 玩家系统
        self.player = Player(self.db, user_id=1)

        # 任务系统
        self.quest_mgr = Quest(self.db, user_id=1)

        # AI 助手"凯"
        self.kai = Kai(self.config)

    def init_ui(self):
        """初始化 UI"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局：水平分栏
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 左侧：玩家面板（占 25%）
        self.player_panel = PlayerPanel(self.player)
        self.player_panel.setFixedWidth(350)
        self.player_panel.level_up.connect(self.on_player_level_up)
        main_layout.addWidget(self.player_panel)

        # 中间：任务面板（占 75%）
        self.quest_panel = QuestPanel(self.quest_mgr)
        self.quest_panel.quest_created.connect(self.on_new_quest)
        self.quest_panel.quest_status_changed.connect(self.on_quest_status_changed)
        main_layout.addWidget(self.quest_panel, 1)

        # 创建菜单栏
        self.create_menu_bar()

        # 创建状态栏
        self.create_status_bar()

        # 创建凯悬浮球
        self.create_kai_sphere()

        # 应用样式
        self.apply_styles()

        # 对话窗口（初始为 None）
        self.chat_dialog = None


    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")

        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        export_action = QAction("导出数据", self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)

        import_action = QAction("导入数据", self)
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)

        file_menu.addSeparator()

        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")

        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("准备就绪")

    def create_kai_sphere(self):
        """创建凯悬浮球"""
        self.kai_sphere = KaiSphere(self)
        self.kai_sphere.clicked.connect(self.show_chat_dialog)

        # 窗口大小改变时重新定位
        self.position_kai_sphere()

    def position_kai_sphere(self):
        """定位凯悬浮球到右下角"""
        if hasattr(self, 'kai_sphere'):
            x = self.width() - self.kai_sphere.width() - 30
            y = self.height() - self.kai_sphere.height() - 80  # 留出状态栏空间
            self.kai_sphere.move(x, y)
            self.kai_sphere.raise_()  # 置顶显示

    def apply_styles(self):
        """应用全局样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QMenuBar {
                background-color: #f8f8f8;
                border-bottom: 1px solid #ddd;
                padding: 5px;
            }
            QMenuBar::item {
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QStatusBar {
                background-color: #f8f8f8;
                border-top: 1px solid #ddd;
            }
        """)

    def load_data(self):
        """加载数据"""
        # 更新状态栏
        quest_stats = self.quest_mgr.get_quest_stats()
        status_text = f"等级 Lv.{self.player.level} | 任务: {quest_stats['total']} 个"
        self.status_bar.showMessage(status_text)

    # ==================== 事件处理 ====================

    def on_player_level_up(self, new_level: int):
        """玩家升级事件"""
        QMessageBox.information(
            self,
            "恭喜升级！",
            f"恭喜！你已经升到 Lv.{new_level} 了！\n\n继续加油！"
        )
        # 刷新状态栏
        self.load_data()

    def on_quest_status_changed(self):
        """任务状态改变事件"""
        # 刷新玩家面板（可能有经验值或属性变化）
        self.player_panel.refresh()
        # 刷新状态栏
        self.load_data()

    def on_new_quest(self):
        """新建任务"""
        from PyQt5.QtWidgets import QInputDialog

        # 简单输入对话框
        title, ok = QInputDialog.getText(self, "新建任务", "请输入任务名称:")

        if ok and title:
            # 创建任务
            quest_id = self.quest_mgr.create_quest(
                name=title,
                description="",
                quest_type="side",
                created_by="user"
            )

            QMessageBox.information(self, "成功", f"任务「{title}」创建成功！")

            # 刷新任务面板
            self.quest_panel.refresh()
            self.load_data()

    def show_settings(self):
        """显示设置对话框"""
        QMessageBox.information(self, "设置", "设置功能开发中...")

    def export_data(self):
        """导出数据"""
        QMessageBox.information(self, "导出", "数据导出功能开发中...")

    def import_data(self):
        """导入数据"""
        QMessageBox.information(self, "导入", "数据导入功能开发中...")

    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h2>启航者 (Voyager)</h2>
        <p>版本: 1.0.0</p>
        <p>一个将个人成长过程游戏化的桌面应用</p>
        <br>
        <p><b>核心特点:</b></p>
        <ul>
            <li>完全本地化 - 所有数据本地存储</li>
            <li>隐私优先 - 无需云端同步</li>
            <li>离线可用 - 无网络也能使用</li>
            <li>AI 可选 - 可配置智谱 AI 增强体验</li>
        </ul>
        <br>
        <p>© 2024 Voyager Team</p>
        """
        QMessageBox.about(self, "关于 Voyager", about_text)

    def show_chat_dialog(self):
        """显示对话窗口"""
        if self.chat_dialog is None:
            # 创建对话窗口
            self.chat_dialog = ChatDialog(self.kai, self)

        # 显示窗口
        self.chat_dialog.show()
        self.chat_dialog.raise_()
        self.chat_dialog.activateWindow()

    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        # 重新定位凯悬浮球
        self.position_kai_sphere()

    def closeEvent(self, event):
        """关闭事件"""
        reply = QMessageBox.question(
            self,
            "确认退出",
            "确定要退出启航者吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# 测试代码
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
