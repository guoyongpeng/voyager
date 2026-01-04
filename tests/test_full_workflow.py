"""
完整工作流测试 - 演示从任务拆解到完成奖励的全流程
"""

import sys
import os

# 设置 UTF-8 编码（Windows 控制台兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.db_manager import DatabaseManager
from src.core.player import Player
from src.core.quest import Quest
from src.ai.kai import Kai


def print_section(title: str):
    """打印章节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_substep(step: str):
    """打印子步骤"""
    print(f"\n→ {step}")
    print("-" * 70)


def main():
    """完整工作流测试"""

    print_section("启航者 (Voyager) - 完整工作流测试")

    # ==================== 第一步：初始化系统 ====================
    print_substep("第一步：初始化系统")

    db = DatabaseManager("data/voyager_test.db")
    print("✅ 数据库初始化完成")

    player = Player(db, user_id=1)
    print("✅ 玩家系统加载完成")

    quest_mgr = Quest(db, user_id=1)
    print("✅ 任务系统加载完成")

    kai = Kai(config_manager=None)  # 无配置，默认使用本地引擎
    print("✅ AI 助手\"凯\"初始化完成（本地规则引擎模式）")

    print("\n【玩家初始状态】")
    print(f"  等级: Lv.{player.level}")
    print(f"  经验: {player.current_xp} XP")
    print(f"  属性: {player.get_attribute_summary()}")

    # ==================== 第二步：任务拆解 ====================
    print_substep("第二步：任务拆解 - 用户提出目标")

    goal = "学习 Python 编程"
    print(f"用户目标: \"{goal}\"")

    # 步骤 1：AI 生成引导问题
    question = kai.decompose_task(goal)
    print(f"\n凯: {question}")

    # 步骤 2：用户回答，AI 生成子任务
    answer = "从基础语法开始"
    print(f"用户: {answer}")

    subtasks = kai.decompose_task(goal, answer)
    print(f"\n凯生成了 {len(subtasks)} 个子任务:")
    for i, task in enumerate(subtasks, 1):
        print(f"  {i}. {task['name']}")
        print(f"     → {task['description']}")

    # ==================== 第三步：创建任务 ====================
    print_substep("第三步：批量创建任务到系统")

    # 创建主线任务
    main_quest_id = quest_mgr.create_quest(
        name=goal,
        description="通过学习 Python 提升编程能力",
        quest_type="main",
        created_by="user"
    )
    print(f"✅ 创建主线任务 (ID: {main_quest_id}): {goal}")

    # 创建子任务
    sub_quest_ids = []
    for task in subtasks:
        quest_id = quest_mgr.create_quest(
            name=task['name'],
            description=task['description'],
            quest_type="side",
            parent_quest_id=main_quest_id,
            created_by="ai"
        )
        sub_quest_ids.append(quest_id)
        print(f"✅ 创建子任务 (ID: {quest_id}): {task['name']}")

    # ==================== 第四步：任务执行 ====================
    print_substep("第四步：开始执行任务")

    # 选择第一个子任务开始
    first_quest_id = sub_quest_ids[0]
    first_quest = quest_mgr.get_quest(first_quest_id)

    print(f"开始任务: {first_quest['title']}")
    quest_mgr.start_quest(first_quest_id)
    print("✅ 任务状态已更新为\"进行中\"")

    # 获取 AI 建议
    suggestion = kai.help_with_task(first_quest['title'], first_quest['description'])
    print(f"\n凯的建议:\n  {suggestion}")

    # ==================== 第五步：情绪检测与关怀 ====================
    print_substep("第五步：用户互动 - 情绪检测")

    user_msg = "今天学了一天有点累，但还是坚持看完了文档"
    print(f"用户消息: \"{user_msg}\"")

    emotion_result = kai.analyze_emotion(user_msg)
    if emotion_result:
        print(f"\n凯检测到情绪: {emotion_result.get('emotion', '未知')}")
        print(f"凯: {emotion_result.get('suggestion', '')}")

        if 'tasks' in emotion_result:
            print("\n推荐的放松任务:")
            for task in emotion_result['tasks']:
                print(f"  - {task['name']}")
    else:
        print("凯: 看起来你状态不错，继续加油！")

    # ==================== 第六步：完成任务与奖励 ====================
    print_substep("第六步：完成任务并获得奖励")

    summary = """
    今天学习了 Python 的基础语法，包括变量、数据类型、运算符等。
    通过查阅官方文档和教程，理解了 Python 的设计哲学。
    虽然过程中遇到了一些概念上的困惑，但通过实践和反复阅读，最终掌握了核心知识点。
    写了几个简单的示例代码进行练习，加深了理解。
    """

    print(f"用户提交心得: \n{summary.strip()}")

    # AI 评判奖励
    reward = kai.judge_completion(first_quest['title'], summary)

    print(f"\n【凯的评价】")
    print(f"  评语: {reward['feedback_text']}")
    print(f"  经验值: +{reward['xp_awarded']} XP")
    print(f"  属性点: {reward['attributes_awarded']}")

    # 完成任务
    completion_result = quest_mgr.complete_quest(
        quest_id=first_quest_id,
        summary=summary.strip(),
        xp_awarded=reward['xp_awarded'],
        attributes_awarded=reward['attributes_awarded'],
        ai_feedback=reward['feedback_text']
    )
    print(f"\n✅ 任务完成记录已保存 (ID: {completion_result['completion_id']})")

    # ==================== 第七步：玩家成长 ====================
    print_substep("第七步：玩家获得奖励并成长")

    print(f"【奖励前状态】")
    print(f"  等级: Lv.{player.level}")
    print(f"  经验: {player.current_xp} XP")
    old_attrs = player.get_attributes()

    # 增加经验值
    level_result = player.add_xp(reward['xp_awarded'])
    print(f"\n增加经验值: +{reward['xp_awarded']} XP")

    # 检查升级
    if level_result['level_up']:
        print(f"\n🎉 恭喜升级！")
        print(f"  新等级: Lv.{level_result['new_level']}")
        print(f"  升级奖励: {level_result['rewards']}")
    else:
        print(f"  距离下一级还需: {level_result['xp_to_next_level']} XP")

    # 增加属性点
    if reward['attributes_awarded']:
        player.add_attributes(reward['attributes_awarded'])
        print(f"\n增加属性点: {reward['attributes_awarded']}")

    print(f"\n【奖励后状态】")
    print(f"  等级: Lv.{player.level}")
    print(f"  经验: {player.current_xp} / {player.calculate_xp_for_level(player.level + 1)} XP")
    print(f"  进度: {int(player.get_progress_to_next_level() * 100)}%")

    new_attrs = player.get_attributes()
    print(f"\n  属性变化:")
    for attr_key, attr_name in [
        ('knowledge', '知识'),
        ('expression', '表达'),
        ('empathy', '共情'),
        ('perseverance', '毅力'),
        ('courage', '勇气')
    ]:
        old_val = old_attrs.get(attr_key, 0)
        new_val = new_attrs.get(attr_key, 0)
        change = new_val - old_val
        change_str = f"(+{change})" if change > 0 else ""
        print(f"    {attr_name}: {old_val} → {new_val} {change_str}")

    # ==================== 第八步：系统统计 ====================
    print_substep("第八步：查看系统统计")

    quest_stats = quest_mgr.get_quest_stats()
    print(f"【任务统计】")
    print(f"  总任务数: {quest_stats['total']}")
    print(f"  待开始: {quest_stats.get('not_started', 0)}")
    print(f"  进行中: {quest_stats.get('in_progress', 0)}")
    print(f"  已完成: {quest_stats.get('completed', 0)}")
    print(f"  已放弃: {quest_stats.get('abandoned', 0)}")

    print(f"\n【任务类型分布】")
    print(f"  主线任务: {quest_stats['by_type'].get('main', 0)}")
    print(f"  支线任务: {quest_stats['by_type'].get('side', 0)}")
    print(f"  每日任务: {quest_stats['by_type'].get('daily', 0)}")

    player_info = player.get_player_info()
    print(f"\n【玩家完整信息】")
    print(f"  用户ID: {player_info['user_id']}")
    print(f"  等级: Lv.{player_info['level']}")
    print(f"  当前经验: {player_info['current_xp']} XP")
    print(f"  累计经验: {player_info['total_xp']} XP")
    print(f"  下级所需: {player_info['xp_to_next_level']} XP")
    print(f"  总属性点: {player_info['total_attribute_points']}")

    # ==================== 完成 ====================
    print_section("测试完成！")

    print("\n✅ 完整工作流测试成功！")
    print("\n【测试覆盖的功能】")
    print("  1. ✅ 数据库初始化与连接")
    print("  2. ✅ 玩家系统加载")
    print("  3. ✅ 任务系统加载")
    print("  4. ✅ AI 助手\"凯\"初始化（本地引擎）")
    print("  5. ✅ 任务拆解（两步流程）")
    print("  6. ✅ 任务创建（主线 + 子任务）")
    print("  7. ✅ 任务状态管理（开始任务）")
    print("  8. ✅ AI 执行建议")
    print("  9. ✅ 情绪检测与关怀")
    print(" 10. ✅ 任务完成与心得记录")
    print(" 11. ✅ 奖励计算（XP + 属性点）")
    print(" 12. ✅ 玩家成长（经验值、升级、属性）")
    print(" 13. ✅ 统计数据查询")

    print("\n🎮 系统核心功能全部正常运行！")
    print("=" * 70)


if __name__ == "__main__":
    main()
