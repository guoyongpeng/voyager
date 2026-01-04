"""
助手引擎抽象基类
定义"凯"助手的核心能力接口
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseEngine(ABC):
    """助手引擎抽象基类"""

    @abstractmethod
    def decompose_task_step1(self, goal: str) -> str:
        """
        任务拆解步骤1：生成引导问题

        Args:
            goal: 用户的目标描述

        Returns:
            str: 引导性问题
        """
        pass

    @abstractmethod
    def decompose_task_step2(self, goal: str, answer: str) -> List[Dict]:
        """
        任务拆解步骤2：生成子任务列表

        Args:
            goal: 用户的目标描述
            answer: 用户对引导问题的回答

        Returns:
            List[Dict]: 子任务列表，每个任务包含 name 和 description
        """
        pass

    @abstractmethod
    def detect_emotion(self, user_input: str) -> Dict:
        """
        情绪检测与任务推荐

        Args:
            user_input: 用户输入的文本

        Returns:
            Dict: 包含情绪类型、建议文本和推荐任务的字典
        """
        pass

    @abstractmethod
    def suggest_for_task(self, task_name: str, description: str = "") -> str:
        """
        为任务提供执行建议

        Args:
            task_name: 任务名称
            description: 任务描述（可选）

        Returns:
            str: 建议文本
        """
        pass

    @abstractmethod
    def calculate_reward(self, task_name: str, summary: str) -> Dict:
        """
        计算任务完成后的奖励

        Args:
            task_name: 任务名称
            summary: 用户的完成总结

        Returns:
            Dict: 包含 xp_awarded（经验值）、attributes_awarded（属性点）
                  和 feedback_text（激励评语）
        """
        pass
