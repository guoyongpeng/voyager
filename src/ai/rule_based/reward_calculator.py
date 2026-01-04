"""
奖励计算器 - 基于关键词和规则的奖励评分算法
这是本地规则引擎的核心组件，用于计算任务完成后的经验值和属性点奖励
"""

import random
from typing import Dict
from ...constants import REWARD_CONFIG, ATTRIBUTE_KEYS


class RewardCalculator:
    """基于规则的奖励计算器"""

    # 属性关键词映射（用于从用户心得中检测属性）
    KEYWORD_ATTRIBUTES = {
        "knowledge": [
            "学", "学习", "研究", "分析", "查资料", "理解", "掌握",
            "阅读", "思考", "总结", "记录", "笔记", "知识", "文档",
            "教程", "原理", "概念", "方法"
        ],
        "expression": [
            "沟通", "分享", "写作", "请教", "交流", "表达", "讨论",
            "发言", "演讲", "报告", "展示", "合作", "协作", "团队",
            "解释", "说明", "传达"
        ],
        "empathy": [
            "帮助", "倾听", "理解", "支持", "关心", "安慰", "陪伴",
            "共情", "感受", "换位思考", "体谅", "包容", "温暖",
            "鼓励", "关怀", "同情"
        ],
        "perseverance": [
            "坚持", "克服", "困难", "挣扎", "继续", "努力", "毅力",
            "不放弃", "挑战", "坚韧", "忍耐", "持续", "积累",
            "磨练", "锻炼", "反复"
        ],
        "courage": [
            "挑战", "第一次", "害怕", "突破", "尝试", "勇气", "勇敢",
            "冒险", "未知", "恐惧", "改变", "创新", "大胆",
            "决心", "突破舒适区", "探索"
        ]
    }

    # 激励评语模板（按属性分类）
    FEEDBACK_TEMPLATES = {
        "knowledge": [
            "看得出你认真学习了，知识储备+1！",
            "学习的态度很棒，继续保持这份求知欲~",
            "掌握新知识的感觉很好吧？你又进步了！",
            "善于总结和思考，这是高效学习的关键！"
        ],
        "expression": [
            "善于表达和分享，这很棒！",
            "你的沟通能力在提升，继续加油！",
            "能清晰地表达想法，这是很重要的能力！",
            "分享让知识更有价值，做得很好！"
        ],
        "empathy": [
            "你的共情能力让人温暖~",
            "善解人意是一种珍贵的品质！",
            "能理解他人的感受，你真的很棒！",
            "这份关怀会让世界变得更美好！"
        ],
        "perseverance": [
            "坚持下来了，这份毅力值得赞赏！",
            "克服困难的过程很辛苦，但你做到了！",
            "持之以恒是成功的关键，继续保持！",
            "每一次坚持都是在积累力量！"
        ],
        "courage": [
            "勇于挑战，这是成长的第一步！",
            "突破舒适区需要勇气，你做得很好！",
            "敢于尝试新事物，这份勇气很可贵！",
            "每一次尝试都是在拓展可能性！"
        ]
    }

    # 通用激励评语（当没有明显属性时使用）
    GENERAL_FEEDBACKS = [
        "完成了任务，继续加油！",
        "每一步前进都值得庆祝~",
        "你在稳步成长，做得很好！",
        "坚持做自己想做的事，真棒！",
        "又向目标迈进了一步！"
    ]

    def __init__(self):
        self.base_xp = REWARD_CONFIG['base_xp']
        self.max_bonus_xp = REWARD_CONFIG['max_bonus_xp']
        self.min_attr_points = REWARD_CONFIG['min_attribute_points']
        self.max_attr_points = REWARD_CONFIG['max_attribute_points']
        self.words_per_xp = REWARD_CONFIG['words_per_xp']

    def calculate_reward(self, task_name: str, user_summary: str) -> Dict:
        """
        计算任务完成后的奖励

        Args:
            task_name: 任务名称
            user_summary: 用户完成任务后的心得体会

        Returns:
            Dict: {
                "xp_awarded": int,  # 总经验值
                "attributes_awarded": Dict[str, int],  # 属性点字典
                "feedback_text": str  # 激励评语
            }
        """
        # 1. 计算基础经验值
        base_xp = self.base_xp

        # 2. 计算额外经验值（根据总结长度）
        summary_length = len(user_summary.strip())
        bonus_xp = min(self.max_bonus_xp, summary_length // self.words_per_xp)

        total_xp = base_xp + bonus_xp

        # 3. 计算属性点（基于关键词匹配）
        attributes = self._calculate_attributes(user_summary)

        # 4. 生成激励评语
        feedback = self._generate_feedback(attributes, summary_length)

        return {
            "xp_awarded": total_xp,
            "attributes_awarded": attributes,
            "feedback_text": feedback
        }

    def _calculate_attributes(self, user_summary: str) -> Dict[str, int]:
        """
        基于关键词匹配计算属性点

        Args:
            user_summary: 用户心得

        Returns:
            Dict[str, int]: 属性点字典
        """
        attributes = {}

        for attr, keywords in self.KEYWORD_ATTRIBUTES.items():
            # 统计该属性关键词的出现次数
            count = sum(1 for kw in keywords if kw in user_summary)

            if count > 0:
                # 计算属性点：基础分 + 关键词数量 * 3，上限20点
                points = min(
                    self.max_attr_points,
                    self.min_attr_points + count * 3
                )
                attributes[attr] = points

        return attributes

    def _generate_feedback(self, attributes: Dict[str, int], summary_length: int) -> str:
        """
        生成个性化激励评语

        Args:
            attributes: 属性点字典
            summary_length: 心得长度

        Returns:
            str: 激励评语
        """
        # 如果没有检测到属性，使用通用评语
        if not attributes:
            return random.choice(self.GENERAL_FEEDBACKS)

        # 选择得分最高的属性
        main_attr = max(attributes, key=attributes.get)

        # 从对应属性的评语模板中随机选择一条
        feedbacks = self.FEEDBACK_TEMPLATES.get(main_attr, self.GENERAL_FEEDBACKS)
        feedback = random.choice(feedbacks)

        # 如果心得特别长（超过200字），额外鼓励
        if summary_length > 200:
            feedback += " 这么详细的总结，看得出你很用心！"

        return feedback

    def get_attribute_summary(self, attributes: Dict[str, int]) -> str:
        """
        生成属性增长的文字总结

        Args:
            attributes: 属性点字典

        Returns:
            str: 属性增长总结
        """
        if not attributes:
            return "暂无属性增长"

        from ...constants import ATTRIBUTES

        parts = []
        for attr, points in attributes.items():
            attr_name = ATTRIBUTES.get(attr, attr)
            parts.append(f"{attr_name}+{points}")

        return "、".join(parts)


# 用于测试的示例代码
if __name__ == "__main__":
    calculator = RewardCalculator()

    # 测试案例1：学习类任务
    result1 = calculator.calculate_reward(
        "学习 Python 基础",
        "今天学习了 Python 的基础语法，通过查资料和看教程，理解了变量、循环和函数的概念。"
        "虽然过程中遇到了一些困难，但坚持下来了。还尝试写了第一个小程序，很有成就感！"
    )
    print("测试案例1:")
    print(f"XP: {result1['xp_awarded']}")
    print(f"属性: {result1['attributes_awarded']}")
    print(f"评语: {result1['feedback_text']}")
    print()

    # 测试案例2：简短总结
    result2 = calculator.calculate_reward(
        "跑步10分钟",
        "完成了"
    )
    print("测试案例2:")
    print(f"XP: {result2['xp_awarded']}")
    print(f"属性: {result2['attributes_awarded']}")
    print(f"评语: {result2['feedback_text']}")
