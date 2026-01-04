"""
AI 助手"凯" - 统一接口
根据配置自动选择本地引擎或 LLM 增强引擎
"""

from typing import Union, List, Dict
from .base_engine import BaseEngine
from .local_engine import LocalEngine
from .dialogue_templates import DialogueTemplates


class Kai:
    """AI 助手"凯"的统一接口"""

    def __init__(self, config_manager=None):
        """
        初始化"凯"助手

        Args:
            config_manager: 配置管理器（可选，用于检测 AI Key 配置）
        """
        self.config = config_manager
        self.templates = DialogueTemplates()
        self.engine = self._init_engine()

    def _init_engine(self) -> BaseEngine:
        """
        根据配置初始化引擎

        Returns:
            BaseEngine: 助手引擎实例
        """
        # 检查是否配置了 AI Key
        if self.config and self.config.has_ai_key():
            # 如果配置了 AI Key，使用 LLM 增强引擎（暂未实现）
            # from .llm_engine import LLMEngine
            # return LLMEngine(self.config)
            print("[提示] AI 增强模式暂未实现，使用本地引擎")
            return LocalEngine()
        else:
            # 默认使用本地规则引擎
            return LocalEngine()

    # ==================== 核心能力方法 ====================

    def decompose_task(
        self,
        goal: str,
        answer: str = None
    ) -> Union[str, List[Dict]]:
        """
        任务拆解（两步式）

        Args:
            goal: 用户的目标
            answer: 用户对引导问题的回答（可选）

        Returns:
            str: 引导问题（当 answer 为 None 时）
            List[Dict]: 子任务列表（当提供 answer 时）
        """
        if answer is None:
            # 步骤1：生成引导问题
            return self.engine.decompose_task_step1(goal)
        else:
            # 步骤2：生成子任务列表
            return self.engine.decompose_task_step2(goal, answer)

    def analyze_emotion(self, user_input: str) -> Dict:
        """
        分析用户情绪并推荐任务

        Args:
            user_input: 用户输入

        Returns:
            Dict: 情绪分析结果和任务推荐
        """
        return self.engine.detect_emotion(user_input)

    def help_with_task(self, task_name: str, description: str = "") -> str:
        """
        为任务提供执行建议

        Args:
            task_name: 任务名称
            description: 任务描述（可选）

        Returns:
            str: 建议文本
        """
        return self.engine.suggest_for_task(task_name, description)

    def judge_completion(self, task_name: str, summary: str) -> Dict:
        """
        评判任务完成情况并计算奖励

        Args:
            task_name: 任务名称
            summary: 用户的完成总结

        Returns:
            Dict: 奖励详情（XP、属性点、激励评语）
        """
        return self.engine.calculate_reward(task_name, summary)

    # ==================== 对话相关方法 ====================

    def greet(self) -> str:
        """获取问候语"""
        return self.templates.get_greeting()

    def encourage(self) -> str:
        """获取鼓励语"""
        return self.templates.get_encouragement()

    def celebrate_task(self) -> str:
        """获取任务完成庆祝语"""
        return self.templates.get_celebration()

    def celebrate_level_up(self, new_level: int) -> str:
        """
        获取升级庆祝语

        Args:
            new_level: 新等级

        Returns:
            str: 升级消息
        """
        return self.templates.get_level_up_message(new_level)

    def guide(self) -> str:
        """获取引导语"""
        return self.templates.get_guidance()

    def comfort(self) -> str:
        """获取安慰语"""
        return self.templates.get_comfort()

    def say_goodbye(self) -> str:
        """获取再见语"""
        return self.templates.get_farewell()

    # ==================== 实用方法 ====================

    def get_mode(self) -> str:
        """
        获取当前运行模式

        Returns:
            str: "local" 或 "ai_enhanced"
        """
        return "local"  # 暂时只有本地模式

    def is_ai_enabled(self) -> bool:
        """
        检查是否启用了 AI 增强功能

        Returns:
            bool: True 表示使用 AI，False 表示本地规则引擎
        """
        return False  # 暂时只有本地模式

    def get_capabilities(self) -> List[str]:
        """
        获取"凯"的能力列表

        Returns:
            List[str]: 能力列表
        """
        return [
            "任务拆解（将大目标分解为具体子任务）",
            "情绪检测（识别情绪并推荐放松任务）",
            "任务建议（提供执行指导和技巧）",
            "奖励评判（智能计算经验值和属性点）",
            "对话陪伴（鼓励、安慰、庆祝等）"
        ]


# 用于测试的示例代码
if __name__ == "__main__":
    print("=" * 60)
    print("AI 助手 '凯' 完整功能测试")
    print("=" * 60)

    kai = Kai()

    print(f"\n运行模式: {kai.get_mode()}")
    print(f"AI 增强: {kai.is_ai_enabled()}")
    print("\n能力列表:")
    for cap in kai.get_capabilities():
        print(f"  - {cap}")

    print("\n" + "-" * 60)
    print("【对话测试】")
    print(f"问候: {kai.greet()}")
    print(f"鼓励: {kai.encourage()}")
    print(f"庆祝: {kai.celebrate_task()}")
    print(f"升级: {kai.celebrate_level_up(5)}")

    print("\n" + "-" * 60)
    print("【任务拆解测试】")
    goal = "学习 Python 编程"
    question = kai.decompose_task(goal)
    print(f"目标: {goal}")
    print(f"引导问题: {question}")
    print(f"用户回答: 从基础语法开始")
    subtasks = kai.decompose_task(goal, "从基础语法开始")
    print("子任务:")
    for i, task in enumerate(subtasks, 1):
        print(f"  {i}. {task['name']}")

    print("\n" + "-" * 60)
    print("【情绪分析测试】")
    user_input = "今天压力好大"
    emotion = kai.analyze_emotion(user_input)
    if emotion:
        print(f"输入: {user_input}")
        print(f"情绪: {emotion.get('emotion')}")
        print(f"建议: {emotion.get('suggestion')}")

    print("\n" + "-" * 60)
    print("【任务建议测试】")
    task_name = "每天跑步 30 分钟"
    suggestion = kai.help_with_task(task_name)
    print(f"任务: {task_name}")
    print(f"建议: {suggestion}")

    print("\n" + "-" * 60)
    print("【奖励计算测试】")
    task_name = "学习 Python 列表"
    summary = "今天学习了列表操作，通过练习掌握了添加、删除等方法，虽然有点困难但坚持下来了"
    reward = kai.judge_completion(task_name, summary)
    print(f"任务: {task_name}")
    print(f"经验值: {reward['xp_awarded']} XP")
    print(f"属性: {reward['attributes_awarded']}")
    print(f"评语: {reward['feedback_text']}")

    print("\n" + "=" * 60)
    print("✅ '凯' 助手所有功能测试完成！")
    print("=" * 60)
