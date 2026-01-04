"""
本地规则引擎 - 整合所有本地规则组件
默认的助手引擎，无需 AI API 即可完整使用
"""

from typing import List, Dict
from .base_engine import BaseEngine
from .rule_based.task_decomposer import TaskDecomposer
from .rule_based.emotion_detector import EmotionDetector
from .rule_based.suggestion_db import SuggestionDB
from .rule_based.reward_calculator import RewardCalculator


class LocalEngine(BaseEngine):
    """本地规则引擎（完全离线，隐私优先）"""

    def __init__(self):
        """初始化所有本地规则组件"""
        self.task_decomposer = TaskDecomposer()
        self.emotion_detector = EmotionDetector()
        self.suggestion_db = SuggestionDB()
        self.reward_calculator = RewardCalculator()

    def decompose_task_step1(self, goal: str) -> str:
        """
        任务拆解步骤1：生成引导问题

        Args:
            goal: 用户的目标描述

        Returns:
            str: 引导性问题
        """
        return self.task_decomposer.decompose_step1(goal)

    def decompose_task_step2(self, goal: str, answer: str = "") -> List[Dict]:
        """
        任务拆解步骤2：生成子任务列表

        Args:
            goal: 用户的目标描述
            answer: 用户对引导问题的回答

        Returns:
            List[Dict]: 子任务列表
        """
        return self.task_decomposer.decompose_step2(goal, answer)

    def detect_emotion(self, user_input: str) -> Dict:
        """
        情绪检测与任务推荐

        Args:
            user_input: 用户输入的文本

        Returns:
            Dict: 情绪检测结果和任务推荐
        """
        return self.emotion_detector.detect(user_input)

    def suggest_for_task(self, task_name: str, description: str = "") -> str:
        """
        为任务提供执行建议

        Args:
            task_name: 任务名称
            description: 任务描述（可选）

        Returns:
            str: 建议文本
        """
        return self.suggestion_db.get_suggestion(task_name, description)

    def calculate_reward(self, task_name: str, summary: str) -> Dict:
        """
        计算任务完成后的奖励

        Args:
            task_name: 任务名称
            summary: 用户的完成总结

        Returns:
            Dict: 奖励详情（XP、属性点、激励评语）
        """
        return self.reward_calculator.calculate_reward(task_name, summary)

    def get_engine_info(self) -> Dict:
        """
        获取引擎信息（用于调试）

        Returns:
            Dict: 引擎信息
        """
        return {
            "type": "LocalEngine",
            "mode": "offline",
            "features": [
                "任务拆解（基于模板）",
                "情绪检测（关键词匹配）",
                "任务建议（预设数据库）",
                "奖励计算（规则算法）"
            ],
            "ai_required": False
        }


# 用于测试的示例代码
if __name__ == "__main__":
    print("=" * 60)
    print("本地引擎完整流程测试")
    print("=" * 60)

    engine = LocalEngine()

    # 1. 测试任务拆解
    print("\n【1. 任务拆解测试】")
    goal = "学习 Python 编程"
    print(f"目标: {goal}")

    question = engine.decompose_task_step1(goal)
    print(f"引导问题: {question}")

    answer = "想从基础语法开始"
    subtasks = engine.decompose_task_step2(goal, answer)
    print(f"用户回答: {answer}")
    print("生成的子任务:")
    for i, task in enumerate(subtasks, 1):
        print(f"  {i}. {task['name']}")
        print(f"     {task['description']}")

    # 2. 测试情绪检测
    print("\n【2. 情绪检测测试】")
    user_input = "今天开了一天会，头昏脑胀的"
    print(f"用户输入: {user_input}")

    emotion_result = engine.detect_emotion(user_input)
    if emotion_result:
        print(f"检测到情绪: {emotion_result.get('emotion')}")
        print(f"建议: {emotion_result.get('suggestion')}")
        tasks = emotion_result.get('tasks', [])
        if tasks:
            print("推荐任务:")
            for task in tasks:
                print(f"  - {task['name']}: {task['description']}")
    else:
        print("无特殊情绪检测")

    # 3. 测试任务建议
    print("\n【3. 任务建议测试】")
    task_name = "学习 Python 基础语法"
    print(f"任务: {task_name}")

    suggestion = engine.suggest_for_task(task_name)
    print(f"建议: {suggestion}")

    # 4. 测试奖励计算
    print("\n【4. 奖励计算测试】")
    task_name = "学习 Python 列表操作"
    summary = (
        "今天学习了 Python 的列表操作，包括添加、删除、切片等。"
        "通过查资料和实践，理解了列表的工作原理。"
        "虽然遇到了一些困难，但坚持下来了，写了几个小程序练习。"
    )
    print(f"任务: {task_name}")
    print(f"总结: {summary}")

    reward = engine.calculate_reward(task_name, summary)
    print(f"\n奖励结果:")
    print(f"  经验值: {reward['xp_awarded']} XP")
    print(f"  属性点: {reward['attributes_awarded']}")
    print(f"  评语: {reward['feedback_text']}")

    # 5. 引擎信息
    print("\n【5. 引擎信息】")
    info = engine.get_engine_info()
    print(f"类型: {info['type']}")
    print(f"模式: {info['mode']}")
    print(f"需要 AI: {info['ai_required']}")
    print("功能:")
    for feature in info['features']:
        print(f"  - {feature}")

    print("\n" + "=" * 60)
    print("✅ 本地引擎所有功能测试完成！")
    print("=" * 60)
