"""
创建测试数据 - 用于演示UI
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.db_manager import DatabaseManager
from src.core.player import Player
from src.core.quest import Quest


def create_test_data():
    """创建测试数据"""
    print("创建测试数据...")

    # 使用主数据库
    db = DatabaseManager("data/voyager.db")
    player = Player(db, user_id=1)
    quest_mgr = Quest(db, user_id=1)

    # 添加一些经验和属性
    print("添加玩家经验和属性...")
    player.add_xp(120)
    player.add_attributes({
        'knowledge': 30,
        'expression': 20,
        'empathy': 25,
        'perseverance': 35,
        'courage': 15
    })

    # 创建一些测试任务
    print("创建测试任务...")

    # 主线任务（进行中）
    main_id = quest_mgr.create_quest(
        name="掌握 Python 编程",
        description="系统学习 Python 语言，成为合格的 Python 开发者",
        quest_type="main",
        created_by="user"
    )
    quest_mgr.start_quest(main_id)
    print(f"  创建主线任务: {main_id}")

    # 支线任务（待开始）
    side_quests = [
        ("学习 PyQt5 GUI 编程", "了解 PyQt5 的基本用法，能够创建简单的桌面应用"),
        ("阅读《代码整洁之道》", "学习如何编写整洁、可维护的代码"),
        ("练习算法题", "每天至少完成一道 LeetCode 算法题")
    ]

    for title, desc in side_quests:
        qid = quest_mgr.create_quest(
            name=title,
            description=desc,
            quest_type="side",
            created_by="user"
        )
        print(f"  创建支线任务: {qid}")

    # 每日任务（进行中）
    daily_id = quest_mgr.create_quest(
        name="今日代码练习",
        description="完成今天的编程练习任务",
        quest_type="daily",
        created_by="user"
    )
    quest_mgr.start_quest(daily_id)
    print(f"  创建每日任务: {daily_id}")

    # 已完成的任务
    completed_id = quest_mgr.create_quest(
        name="配置开发环境",
        description="安装 Python、PyQt5 等开发工具",
        quest_type="side",
        created_by="user"
    )
    quest_mgr.start_quest(completed_id)
    quest_mgr.complete_quest(
        quest_id=completed_id,
        summary="成功安装了所有必需的开发工具，环境配置完成！",
        xp_awarded=50,
        attributes_awarded={'knowledge': 10, 'perseverance': 5},
        ai_feedback="很好！环境搭建是第一步，做得不错！"
    )
    print(f"  创建已完成任务: {completed_id}")

    print("\n测试数据创建完成！")
    print(f"玩家等级: Lv.{player.level}")
    print(f"总经验: {player.total_xp} XP")
    print(f"总属性点: {player.get_total_attribute_points()}")

    stats = quest_mgr.get_quest_stats()
    print(f"\n任务统计:")
    print(f"  总任务数: {stats['total']}")
    print(f"  待开始: {stats.get('pending', 0)}")
    print(f"  进行中: {stats.get('in_progress', 0)}")
    print(f"  已完成: {stats.get('completed', 0)}")


if __name__ == "__main__":
    create_test_data()
