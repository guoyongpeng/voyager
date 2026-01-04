"""
启航者 (Voyager) - 应用入口
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """应用主函数"""
    # 创建应用实例
    app = QApplication(sys.argv)

    # 设置应用信息
    app.setApplicationName("启航者 (Voyager)")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Voyager Team")

    # 创建并显示主窗口
    window = MainWindow()
    window.show()

    # 运行应用事件循环
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
