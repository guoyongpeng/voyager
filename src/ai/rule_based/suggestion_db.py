"""
建议数据库 - 预设的任务执行建议库
根据任务类型提供具体的执行建议和指导
"""

import random
from typing import List


class SuggestionDB:
    """任务建议数据库"""

    # 按任务类型分类的建议库
    SUGGESTIONS = {
        "学习": [
            "可以先从官方文档开始，了解基础概念",
            "尝试跟着教程做一个小项目，实践是最好的老师",
            "加入相关社区或论坛，向他人请教",
            "做好笔记，定期回顾总结",
            "不要急于求成，每天进步一点点就很棒",
            "遇到不懂的地方，多问几个为什么",
            "找一个学习伙伴，互相监督和交流"
        ],
        "运动": [
            "刚开始不要给自己太大压力，循序渐进",
            "记录每次运动的数据，看到进步会更有动力",
            "找个伙伴一起，更容易坚持",
            "准备好合适的装备，让运动更舒适",
            "运动前做好热身，运动后记得拉伸",
            "如果感觉不适，及时休息，不要勉强",
            "制定一个可持续的计划，而不是三天打鱼"
        ],
        "工作": [
            "先把任务拆解成几个小步骤，逐个击破",
            "设定明确的截止时间，给自己适当的紧迫感",
            "专注时关掉不必要的通知，提高效率",
            "遇到难题时，不妨先做其他简单的部分",
            "定期向同事或领导同步进度，及时调整",
            "完成后记得复盘，总结经验教训",
            "不要拖延，现在就开始第一步"
        ],
        "整理": [
            "可以先从最小的一个区域开始，比如书桌一角",
            "准备好收纳工具，分类整理会更高效",
            "断舍离：扔掉、捐赠、或送人不需要的东西",
            "整理的同时，思考如何避免再次杂乱",
            "不要一次性全部整理，容易累垮",
            "拍照记录整理前后的对比，会很有成就感",
            "定期整理，养成习惯比一次性大扫除重要"
        ],
        "阅读": [
            "选择一个安静舒适的环境，更容易专注",
            "可以先看目录和序言，了解整体结构",
            "准备一支笔，随手记录感想和疑问",
            "不用逐字逐句，重点章节可以精读",
            "读完一章后，试着用自己的话总结",
            "和朋友分享书中的观点，加深理解",
            "不要勉强读不喜欢的书，阅读应该是享受"
        ],
        "练习": [
            "制定一个循序渐进的练习计划",
            "每次练习前明确目标，比如今天要掌握什么",
            "记录练习过程中的问题和进步",
            "不要害怕犯错，错误是学习的最好机会",
            "定期回顾之前练习过的内容，巩固记忆",
            "找到自己的薄弱环节，针对性加强",
            "坚持每天练习，哪怕只有10分钟"
        ],
        "创作": [
            "不要追求完美，先完成再说",
            "灵感来了就记下来，哪怕只是只言片语",
            "多看优秀作品，汲取灵感和技巧",
            "给自己设定一个具体的主题或约束",
            "创作遇到瓶颈时，出去走走换换心情",
            "不要害怕别人的评价，勇敢表达自己",
            "定期分享作品，听听他人的反馈"
        ],
        "社交": [
            "主动一点，大部分人都喜欢被关心",
            "倾听比说话更重要，用心感受对方",
            "真诚最重要，不要刻意迎合",
            "记住对方的喜好和重要日子",
            "约见面时选个双方都方便的时间和地点",
            "聊天时多问开放性问题，而不是只回答是或否",
            "维护关系需要时间投入，定期联系很重要"
        ],
        "休息": [
            "放下手机，真正地放松自己",
            "可以听听音乐、冥想或者只是发呆",
            "不要有负罪感，休息是为了更好地前进",
            "泡个热水澡或喝杯热饮，放松身心",
            "到户外走走，亲近大自然",
            "做一些不需要动脑的事情，让思绪放空",
            "保证充足的睡眠，这是最好的休息"
        ],
        "计划": [
            "先确定最重要的 2-3 个目标",
            "把大目标拆解成具体的行动步骤",
            "每个步骤设定可量化的标准和时间节点",
            "预留缓冲时间，计划不要排太满",
            "定期回顾和调整计划，保持灵活性",
            "写下来比只在脑子里想更有用",
            "执行比完美的计划更重要"
        ],
        "通用": [
            "想清楚为什么要做这件事，动机很重要",
            "分步骤进行，不要想着一口吃成胖子",
            "遇到困难很正常，坚持下去就好",
            "可以寻求他人的帮助或建议",
            "记录过程和收获，方便日后回顾",
            "给自己设定一个小奖励，完成后犒劳一下",
            "保持积极的心态，相信自己能做到"
        ]
    }

    # 类别关键词映射（用于识别任务类型）
    CATEGORY_KEYWORDS = {
        "学习": ["学", "学习", "掌握", "了解", "研究", "熟悉", "理解"],
        "运动": ["运动", "锻炼", "跑步", "健身", "瑜伽", "游泳"],
        "工作": ["工作", "项目", "完成", "交付", "开发", "设计"],
        "整理": ["整理", "打扫", "收纳", "清理", "归纳"],
        "阅读": ["阅读", "读", "看书", "书籍"],
        "练习": ["练习", "训练", "练", "操练"],
        "创作": ["创作", "写", "画", "设计", "制作"],
        "社交": ["朋友", "家人", "社交", "聚会", "约"],
        "休息": ["休息", "放松", "睡觉", "冥想"],
        "计划": ["计划", "规划", "安排", "目标"]
    }

    def detect_category(self, task_name: str, task_description: str = "") -> str:
        """
        检测任务类型

        Args:
            task_name: 任务名称
            task_description: 任务描述（可选）

        Returns:
            str: 类别名称，默认返回"通用"
        """
        combined_text = task_name + " " + task_description

        max_matches = 0
        best_category = "通用"

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            matches = sum(1 for keyword in keywords if keyword in combined_text)
            if matches > max_matches:
                max_matches = matches
                best_category = category

        return best_category

    def get_suggestion(self, task_name: str, task_description: str = "") -> str:
        """
        获取任务执行建议

        Args:
            task_name: 任务名称
            task_description: 任务描述（可选）

        Returns:
            str: 建议文本
        """
        category = self.detect_category(task_name, task_description)
        suggestions = self.SUGGESTIONS.get(category, self.SUGGESTIONS["通用"])

        # 随机选择一条建议
        return random.choice(suggestions)

    def get_multiple_suggestions(
        self,
        task_name: str,
        task_description: str = "",
        count: int = 3
    ) -> List[str]:
        """
        获取多条建议

        Args:
            task_name: 任务名称
            task_description: 任务描述
            count: 返回建议的数量

        Returns:
            List[str]: 建议列表
        """
        category = self.detect_category(task_name, task_description)
        suggestions = self.SUGGESTIONS.get(category, self.SUGGESTIONS["通用"])

        # 随机选择多条建议（不重复）
        count = min(count, len(suggestions))
        return random.sample(suggestions, count)

    def add_custom_suggestion(self, category: str, suggestion: str):
        """
        添加自定义建议（可用于后续扩展）

        Args:
            category: 类别名称
            suggestion: 建议文本
        """
        if category not in self.SUGGESTIONS:
            self.SUGGESTIONS[category] = []

        if suggestion not in self.SUGGESTIONS[category]:
            self.SUGGESTIONS[category].append(suggestion)


# 用于测试的示例代码
if __name__ == "__main__":
    db = SuggestionDB()

    test_cases = [
        ("学习 Python 编程", "从基础语法开始"),
        ("每天跑步 30 分钟", "提高身体素质"),
        ("完成项目文档", "整理需求和设计"),
        ("读完《三体》", "科幻小说"),
        ("练习钢琴", "每天练习 1 小时"),
        ("变得更好", "不知道从哪开始")
    ]

    print("=" * 60)
    print("建议数据库测试")
    print("=" * 60)

    for task_name, task_desc in test_cases:
        category = db.detect_category(task_name, task_desc)
        suggestion = db.get_suggestion(task_name, task_desc)

        print(f"\n任务: {task_name}")
        print(f"描述: {task_desc}")
        print(f"类别: {category}")
        print(f"建议: {suggestion}")

    print("\n" + "=" * 60)
    print("获取多条建议测试")
    print("=" * 60)

    task = "学习 Python"
    suggestions = db.get_multiple_suggestions(task, count=3)
    print(f"\n任务: {task}")
    print("建议:")
    for i, sug in enumerate(suggestions, 1):
        print(f"  {i}. {sug}")
