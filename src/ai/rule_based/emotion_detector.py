"""
情绪检测器 - 基于关键词的情绪识别和任务推荐
分析用户输入中的情绪关键词，主动推荐合适的任务
"""

from typing import Dict, Optional


class EmotionDetector:
    """基于关键词的情绪检测器"""

    # 情绪关键词词库（每种情绪包含多个同义词和相关表达）
    EMOTION_KEYWORDS = {
        "疲惫": [
            "累", "疲惫", "头昏脑胀", "没精神", "困", "疲劳", "乏力",
            "精疲力尽", "筋疲力尽", "身心俱疲", "无力", "倦", "劳累"
        ],
        "压力": [
            "压力", "焦虑", "紧张", "烦", "不安", "担心", "忧虑",
            "心烦", "烦躁", "焦急", "着急", "慌", "压抑", "喘不过气"
        ],
        "迷茫": [
            "迷茫", "不知道", "困惑", "无助", "茫然", "迷失", "找不到方向",
            "不知所措", "无所适从", "彷徨", "迷惑", "摸不着头脑"
        ],
        "消极": [
            "难过", "失落", "沮丧", "难受", "痛苦", "悲伤", "伤心",
            "难熬", "糟糕", "不开心", "郁闷", "低落", "失望", "无望"
        ],
        "孤独": [
            "孤独", "寂寞", "孤单", "一个人", "没人", "空虚", "落寞",
            "孤寂", "冷清", "无人理解"
        ],
        "疲惫": [
            "疲倦", "想休息", "撑不住", "扛不住", "坚持不下去"
        ]
    }

    # 任务推荐映射（针对不同情绪推荐不同类型的任务）
    TASK_RECOMMENDATIONS = {
        "疲惫": {
            "suggestion": "看起来你有些疲惫呢，要不要先放松一下？我给你推荐个小任务~",
            "tasks": [
                {"name": "休息10分钟", "description": "放空自己，什么都不想", "attribute": "perseverance"},
                {"name": "听一首喜欢的音乐", "description": "闭上眼睛，享受音乐", "attribute": "empathy"},
                {"name": "做几个伸展动作", "description": "舒展筋骨，放松身体", "attribute": "courage"}
            ]
        },
        "压力": {
            "suggestion": "感觉到你有些压力，不如先做个深呼吸，整理一下思绪？",
            "tasks": [
                {"name": "写下今天的3件好事", "description": "发现生活中的小确幸", "attribute": "empathy"},
                {"name": "整理桌面", "description": "清理杂物，理清思路", "attribute": "perseverance"},
                {"name": "散步5分钟", "description": "出去走走，换个心情", "attribute": "courage"}
            ]
        },
        "迷茫": {
            "suggestion": "感到迷茫很正常，不如先从小事开始做起？",
            "tasks": [
                {"name": "写下当下的想法", "description": "不评判，只是记录", "attribute": "expression"},
                {"name": "列出最近想做的3件小事", "description": "从简单的开始", "attribute": "knowledge"},
                {"name": "回顾最近的成就", "description": "看看自己已经走了多远", "attribute": "empathy"}
            ]
        },
        "消极": {
            "suggestion": "情绪低落的时候，做点小事情也许会好一些~",
            "tasks": [
                {"name": "给自己泡杯热饮", "description": "温暖一下身体和心灵", "attribute": "empathy"},
                {"name": "看一集喜欢的剧", "description": "暂时转移注意力", "attribute": "empathy"},
                {"name": "做一件很小很小的事", "description": "任何完成的感觉都是进步", "attribute": "perseverance"}
            ]
        },
        "孤独": {
            "suggestion": "一个人的时候，不妨和自己对话，或者联系一个朋友？",
            "tasks": [
                {"name": "给朋友或家人发个消息", "description": "简单的问候也能温暖彼此", "attribute": "expression"},
                {"name": "写日记", "description": "和自己对话，倾听内心", "attribute": "empathy"},
                {"name": "做一件自己喜欢的事", "description": "享受独处的时光", "attribute": "knowledge"}
            ]
        }
    }

    # 积极情绪关键词（用于给予正面反馈）
    POSITIVE_KEYWORDS = [
        "开心", "高兴", "快乐", "兴奋", "激动", "满足", "充实",
        "有成就感", "进步", "完成", "成功", "顺利", "棒", "好"
    ]

    def detect(self, user_input: str) -> Dict:
        """
        检测用户输入中的情绪并推荐任务

        Args:
            user_input: 用户的输入文本

        Returns:
            Dict: {
                "emotion": str,  # 检测到的情绪类型
                "suggestion": str,  # 建议文本
                "tasks": List[Dict],  # 推荐的任务列表
                "is_positive": bool  # 是否为积极情绪
            }
            如果无需推荐，返回空字典 {}
        """
        # 1. 检测积极情绪
        if self._has_positive_emotion(user_input):
            return {
                "emotion": "积极",
                "suggestion": self._get_positive_response(user_input),
                "tasks": [],
                "is_positive": True
            }

        # 2. 检测消极情绪并推荐任务
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            if any(keyword in user_input for keyword in keywords):
                recommendation = self.TASK_RECOMMENDATIONS.get(emotion, {})

                return {
                    "emotion": emotion,
                    "suggestion": recommendation.get("suggestion", ""),
                    "tasks": recommendation.get("tasks", []),
                    "is_positive": False
                }

        # 3. 无特殊情绪，返回空字典
        return {}

    def _has_positive_emotion(self, user_input: str) -> bool:
        """检测是否包含积极情绪关键词"""
        return any(keyword in user_input for keyword in self.POSITIVE_KEYWORDS)

    def _get_positive_response(self, user_input: str) -> str:
        """生成积极情绪的回应"""
        responses = [
            "听起来心情不错！继续保持这份好状态~",
            "太棒了！开心的时候效率也会更高呢！",
            "能感受到你的好心情，继续加油！",
            "这种积极的状态很好，珍惜当下的每一刻！"
        ]

        import random
        return random.choice(responses)

    def get_emotion_summary(self, user_input: str) -> str:
        """
        获取情绪检测的文字总结（用于调试或日志）

        Args:
            user_input: 用户输入

        Returns:
            str: 情绪总结
        """
        result = self.detect(user_input)

        if not result:
            return "未检测到明显情绪"

        if result.get("is_positive"):
            return f"检测到积极情绪：{result['suggestion']}"

        emotion = result.get("emotion", "未知")
        task_count = len(result.get("tasks", []))
        return f"检测到情绪：{emotion}，推荐了 {task_count} 个任务"


# 用于测试的示例代码
if __name__ == "__main__":
    detector = EmotionDetector()

    test_cases = [
        "今天开了一天会，头昏脑胀的。",
        "最近压力好大，不知道怎么办。",
        "感觉好迷茫，不知道自己在干什么。",
        "今天完成了一个重要任务，特别有成就感！",
        "今天天气不错，准备学习Python。"
    ]

    print("=" * 60)
    print("情绪检测器测试")
    print("=" * 60)

    for i, text in enumerate(test_cases, 1):
        print(f"\n测试案例 {i}: {text}")
        result = detector.detect(text)

        if not result:
            print("  -> 无需推荐")
        elif result.get("is_positive"):
            print(f"  -> 情绪: {result['emotion']}")
            print(f"  -> 回应: {result['suggestion']}")
        else:
            print(f"  -> 情绪: {result['emotion']}")
            print(f"  -> 建议: {result['suggestion']}")
            print(f"  -> 推荐任务:")
            for task in result.get("tasks", []):
                print(f"     - {task['name']}: {task['description']}")

    print("\n" + "=" * 60)
