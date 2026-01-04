"""
任务拆解器 - 基于模板的任务拆解引擎
通过关键词匹配识别任务类别，使用预设模板生成子任务
"""

from typing import List, Dict


class TaskDecomposer:
    """基于模板的任务拆解器"""

    # 任务类别关键词映射
    CATEGORY_KEYWORDS = {
        "学习类": ["学", "学习", "掌握", "了解", "研究", "熟悉", "理解", "阅读", "看", "读"],
        "健康类": ["健康", "运动", "锻炼", "减肥", "健身", "跑步", "瑜伽", "睡眠", "休息"],
        "技能类": ["技能", "能力", "提升", "练习", "训练", "培养", "改进", "开发"],
        "工作类": ["工作", "项目", "任务", "完成", "交付", "开发", "设计", "编写"],
        "兴趣类": ["兴趣", "爱好", "娱乐", "游戏", "音乐", "绘画", "摄影", "旅行"],
        "人际类": ["朋友", "家人", "同事", "社交", "沟通", "交流", "聚会", "约会"],
        "生活类": ["生活", "整理", "打扫", "收纳", "做饭", "购物", "家务"],
        "财务类": ["理财", "存钱", "预算", "投资", "记账", "消费", "收入"]
    }

    # 任务模板库（每个类别包含引导问题和子任务模板）
    TEMPLATES = {
        "学习类": {
            "question": "你想学习{目标}的哪个方面？（如基础概念、实践操作、进阶技巧等）",
            "subtasks": [
                {"name": "了解{目标}的基础知识", "description": "查找相关资料、教程或文档"},
                {"name": "动手实践{目标}", "description": "完成一个简单的练习或小项目"},
                {"name": "总结学习心得", "description": "记录收获、难点和下一步计划"}
            ]
        },
        "健康类": {
            "question": "你想从哪方面改善健康？（如运动、饮食、睡眠等）",
            "subtasks": [
                {"name": "制定{目标}计划", "description": "设定具体可行的目标和时间安排"},
                {"name": "执行{目标}行动", "description": "按计划坚持实践，记录每日进度"},
                {"name": "评估和调整", "description": "总结效果，根据实际情况优化计划"}
            ]
        },
        "技能类": {
            "question": "你希望通过什么方式提升{目标}？（如刻意练习、学习课程、实战项目等）",
            "subtasks": [
                {"name": "分析{目标}的核心要素", "description": "明确需要练习的关键技能点"},
                {"name": "设计练习方案", "description": "制定循序渐进的训练计划"},
                {"name": "持续练习并反馈", "description": "每日练习，记录进步和问题"}
            ]
        },
        "工作类": {
            "question": "这个{目标}的优先级和截止时间是什么？",
            "subtasks": [
                {"name": "拆解{目标}的子任务", "description": "将大任务分解为具体可执行的步骤"},
                {"name": "逐步完成各子任务", "description": "按优先级依次推进"},
                {"name": "检查和复盘", "description": "确保质量，总结经验教训"}
            ]
        },
        "兴趣类": {
            "question": "你想如何开始或深入{目标}这个兴趣？",
            "subtasks": [
                {"name": "探索{目标}的入门方式", "description": "了解基础信息或体验课程"},
                {"name": "投入时间享受{目标}", "description": "放松心态，单纯享受过程"},
                {"name": "记录有趣的体验", "description": "拍照、写日记或分享给朋友"}
            ]
        },
        "人际类": {
            "question": "你想通过什么方式加强{目标}的关系？",
            "subtasks": [
                {"name": "主动联系{目标}", "description": "发个消息或约个时间见面"},
                {"name": "倾听和交流", "description": "真诚沟通，了解对方近况"},
                {"name": "维护关系", "description": "定期保持联系，记住重要日子"}
            ]
        },
        "生活类": {
            "question": "你打算如何完成{目标}？需要多长时间？",
            "subtasks": [
                {"name": "准备{目标}所需物品", "description": "列出清单，准备工具或材料"},
                {"name": "执行{目标}", "description": "按步骤完成，保持专注"},
                {"name": "检查成果", "description": "确认完成质量，整理善后"}
            ]
        },
        "财务类": {
            "question": "你的{目标}具体金额和时间规划是什么？",
            "subtasks": [
                {"name": "分析当前{目标}状况", "description": "梳理收入、支出或资产情况"},
                {"name": "制定{目标}计划", "description": "设定可量化的目标和时间表"},
                {"name": "执行并跟踪", "description": "按计划执行，定期复盘调整"}
            ]
        },
        "通用类": {
            "question": "你想如何开始{目标}？有什么具体想法吗？",
            "subtasks": [
                {"name": "明确{目标}的具体目标", "description": "想清楚要达成什么结果"},
                {"name": "分步骤推进{目标}", "description": "一步步完成，不急于求成"},
                {"name": "总结和反思", "description": "记录过程中的收获和改进点"}
            ]
        }
    }

    def detect_category(self, goal: str) -> str:
        """
        通过关键词匹配检测目标所属类别

        Args:
            goal: 用户的目标描述

        Returns:
            str: 类别名称（如"学习类"、"健康类"等），默认返回"通用类"
        """
        max_matches = 0
        best_category = "通用类"

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            # 统计该类别关键词在目标中出现的次数
            matches = sum(1 for keyword in keywords if keyword in goal)

            if matches > max_matches:
                max_matches = matches
                best_category = category

        return best_category

    def decompose_step1(self, goal: str) -> str:
        """
        步骤一：生成引导性问题

        Args:
            goal: 用户的原始目标

        Returns:
            str: 引导性问题
        """
        category = self.detect_category(goal)
        template = self.TEMPLATES[category]

        # 替换模板中的变量
        question = template["question"].format(目标=goal)

        return question

    def decompose_step2(self, goal: str, answer: str = "") -> List[Dict[str, str]]:
        """
        步骤二：生成子任务列表

        Args:
            goal: 用户的原始目标
            answer: 用户对引导问题的回答（可选，用于优化子任务）

        Returns:
            List[Dict]: 子任务列表，每个任务包含 name 和 description
        """
        category = self.detect_category(goal)
        template = self.TEMPLATES[category]

        # 替换模板变量生成子任务
        subtasks = []
        for task_template in template["subtasks"]:
            task = {
                "name": task_template["name"].format(目标=goal),
                "description": task_template["description"]
            }
            subtasks.append(task)

        return subtasks

    def get_category_info(self, goal: str) -> Dict:
        """
        获取目标的类别信息（用于调试或展示）

        Args:
            goal: 用户的目标

        Returns:
            Dict: 包含类别名称和匹配关键词数量
        """
        category = self.detect_category(goal)
        keywords = self.CATEGORY_KEYWORDS.get(category, [])
        matches = [kw for kw in keywords if kw in goal]

        return {
            "category": category,
            "matched_keywords": matches,
            "match_count": len(matches)
        }


# 用于测试的示例代码
if __name__ == "__main__":
    decomposer = TaskDecomposer()

    # 测试案例1：学习类
    print("=" * 50)
    print("测试案例1：学习 Python 编程")
    goal1 = "学习 Python 编程"
    print(f"目标: {goal1}")
    print(f"类别: {decomposer.get_category_info(goal1)}")
    print(f"引导问题: {decomposer.decompose_step1(goal1)}")
    print("子任务:")
    for i, task in enumerate(decomposer.decompose_step2(goal1), 1):
        print(f"  {i}. {task['name']}")
        print(f"     {task['description']}")
    print()

    # 测试案例2：健康类
    print("=" * 50)
    print("测试案例2：每天跑步30分钟")
    goal2 = "每天跑步30分钟"
    print(f"目标: {goal2}")
    print(f"类别: {decomposer.get_category_info(goal2)}")
    print(f"引导问题: {decomposer.decompose_step1(goal2)}")
    print("子任务:")
    for i, task in enumerate(decomposer.decompose_step2(goal2), 1):
        print(f"  {i}. {task['name']}")
        print(f"     {task['description']}")
    print()

    # 测试案例3：通用类
    print("=" * 50)
    print("测试案例3：变得更好")
    goal3 = "变得更好"
    print(f"目标: {goal3}")
    print(f"类别: {decomposer.get_category_info(goal3)}")
    print(f"引导问题: {decomposer.decompose_step1(goal3)}")
    print("子任务:")
    for i, task in enumerate(decomposer.decompose_step2(goal3), 1):
        print(f"  {i}. {task['name']}")
        print(f"     {task['description']}")
