"""
对话模板库 - "凯"的预设话术
提供各种场景下的自然对话模板
"""

import random
from typing import List


class DialogueTemplates:
    """"凯"的对话模板库"""

    # 问候语（根据时间或场景）
    GREETINGS = [
        "你好呀！今天想做些什么？",
        "嗨！有什么可以帮到你的吗？",
        "又见面啦~有什么新计划吗？",
        "你来了！今天感觉怎么样？",
        "很高兴见到你！准备开始今天的旅程了吗？"
    ]

    # 鼓励语（任务进行中或完成后）
    ENCOURAGEMENTS = [
        "做得很好！继续保持~",
        "你很棒！一步步在进步！",
        "坚持下去，你可以的！",
        "每一小步都值得庆祝！",
        "你在变得越来越好！",
        "这份努力不会白费的！",
        "相信自己，你能做到！",
        "加油！离目标又近了一步！"
    ]

    # 任务完成庆祝
    CELEBRATIONS = [
        "太棒了！任务完成！🎉",
        "成功！你做到了！",
        "完成啦！给自己一个大大的赞！",
        "厉害！又解锁了一个成就！",
        "恭喜！这次完成得很漂亮！"
    ]

    # 升级庆祝
    LEVEL_UP_MESSAGES = [
        "恭喜升级！🎊 你变得更强了！",
        "等级提升！继续加油，前方还有更多精彩！",
        "升级成功！你的成长之路越来越宽广！",
        "太棒了！达到了新的高度！"
    ]

    # 引导语（帮助用户明确目标）
    GUIDANCE = [
        "不如先从小目标开始？",
        "我们一起把目标拆解得更具体一些吧~",
        "想清楚第一步要做什么了吗？",
        "试着把想法写下来，会更清晰哦~",
        "可以先问问自己：为什么想做这件事？"
    ]

    # 安慰语（遇到困难时）
    COMFORTS = [
        "遇到困难很正常，休息一下再继续吧~",
        "没关系，每个人都会遇到瓶颈期。",
        "不要太苛责自己，已经做得很好了。",
        "暂时的停滞不是退步，是在积蓄力量。",
        "放慢脚步也没关系，重要的是方向对。"
    ]

    # 提醒语（定期复盘或计划）
    REMINDERS = [
        "好久没见了，最近过得怎么样？",
        "要不要回顾一下最近的进展？",
        "有什么新的想法或计划吗？",
        "记得定期总结，会发现自己的成长哦~"
    ]

    # 再见语
    FAREWELLS = [
        "今天辛苦了！期待下次见面~",
        "休息一下吧，明天继续加油！",
        "拜拜！记得好好照顾自己~",
        "下次再聊！保持这份热情！"
    ]

    # 通用回复（无法识别意图时）
    GENERAL_RESPONSES = [
        "嗯嗯，我在听~",
        "继续说说看？",
        "听起来不错！",
        "然后呢？",
        "理解你的感受~"
    ]

    @staticmethod
    def get_greeting() -> str:
        """获取随机问候语"""
        return random.choice(DialogueTemplates.GREETINGS)

    @staticmethod
    def get_encouragement() -> str:
        """获取随机鼓励语"""
        return random.choice(DialogueTemplates.ENCOURAGEMENTS)

    @staticmethod
    def get_celebration() -> str:
        """获取任务完成庆祝语"""
        return random.choice(DialogueTemplates.CELEBRATIONS)

    @staticmethod
    def get_level_up_message(new_level: int) -> str:
        """
        获取升级庆祝语

        Args:
            new_level: 新等级

        Returns:
            str: 升级消息
        """
        base_msg = random.choice(DialogueTemplates.LEVEL_UP_MESSAGES)
        return f"{base_msg}\n你现在是 Lv.{new_level} 了！"

    @staticmethod
    def get_guidance() -> str:
        """获取引导语"""
        return random.choice(DialogueTemplates.GUIDANCE)

    @staticmethod
    def get_comfort() -> str:
        """获取安慰语"""
        return random.choice(DialogueTemplates.COMFORTS)

    @staticmethod
    def get_reminder() -> str:
        """获取提醒语"""
        return random.choice(DialogueTemplates.REMINDERS)

    @staticmethod
    def get_farewell() -> str:
        """获取再见语"""
        return random.choice(DialogueTemplates.FAREWELLS)

    @staticmethod
    def get_general_response() -> str:
        """获取通用回复"""
        return random.choice(DialogueTemplates.GENERAL_RESPONSES)

    @staticmethod
    def get_task_start_message(task_name: str) -> str:
        """
        获取任务开始提示

        Args:
            task_name: 任务名称

        Returns:
            str: 提示消息
        """
        messages = [
            f"好的！开始'{task_name}'吧，加油！",
            f"准备好了吗？让我们一起完成'{task_name}'！",
            f"'{task_name}'正式开始，相信你能做到！",
            f"很好！'{task_name}'是个不错的目标，开始行动吧！"
        ]
        return random.choice(messages)

    @staticmethod
    def get_task_completion_prompt(task_name: str) -> str:
        """
        获取任务完成提示（要求用户写心得）

        Args:
            task_name: 任务名称

        Returns:
            str: 提示消息
        """
        prompts = [
            f"'{task_name}'完成了！写点心得体会吧，说说你的收获~",
            f"恭喜完成'{task_name}'！简单总结一下过程和感受？",
            f"太棒了！'{task_name}'搞定了！分享一下你的经验吧~",
            f"任务完成！说说做'{task_name}'时有什么发现或困难？"
        ]
        return random.choice(prompts)

    @staticmethod
    def get_attribute_growth_message(attributes: dict) -> str:
        """
        获取属性增长提示

        Args:
            attributes: 属性增长字典 {"knowledge": 10, "courage": 15}

        Returns:
            str: 提示消息
        """
        from ..constants import ATTRIBUTES

        if not attributes:
            return "获得了宝贵的经验！"

        parts = []
        for attr, points in attributes.items():
            attr_name = ATTRIBUTES.get(attr, attr)
            parts.append(f"{attr_name}+{points}")

        attr_text = "、".join(parts)
        return f"属性增长：{attr_text}！"


# 用于测试的示例代码
if __name__ == "__main__":
    print("=" * 60)
    print("对话模板测试")
    print("=" * 60)

    templates = DialogueTemplates()

    print("\n【问候语】")
    for _ in range(3):
        print(f"  - {templates.get_greeting()}")

    print("\n【鼓励语】")
    for _ in range(3):
        print(f"  - {templates.get_encouragement()}")

    print("\n【任务相关】")
    print(f"  开始: {templates.get_task_start_message('学习Python')}")
    print(f"  完成: {templates.get_task_completion_prompt('学习Python')}")

    print("\n【升级消息】")
    print(f"  {templates.get_level_up_message(5)}")

    print("\n【属性增长】")
    print(f"  {templates.get_attribute_growth_message({'knowledge': 10, 'courage': 15})}")

    print("\n" + "=" * 60)
