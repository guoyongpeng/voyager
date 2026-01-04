"""
任务系统 - 管理任务生命周期
"""

from typing import Dict, List, Optional
from datetime import datetime
from ..database.db_manager import DatabaseManager
from ..constants import QUEST_TYPES, QUEST_STATUS


class Quest:
    """任务系统，负责任务的创建、更新、完成等操作"""

    def __init__(self, db_manager: DatabaseManager, user_id: int = 1):
        """
        初始化任务系统

        Args:
            db_manager: 数据库管理器实例
            user_id: 用户ID，默认为1
        """
        self.db = db_manager
        self.user_id = user_id

    def create_quest(
        self,
        name: str,
        description: str = "",
        quest_type: str = "side",
        parent_quest_id: Optional[int] = None,
        created_by: str = "user"
    ) -> int:
        """
        创建新任务

        Args:
            name: 任务名称
            description: 任务描述
            quest_type: 任务类型 (main/side/daily)
            parent_quest_id: 父任务ID（子任务时使用）
            created_by: 创建者 (user/ai)

        Returns:
            int: 新任务的ID
        """
        if quest_type not in QUEST_TYPES:
            quest_type = "side"

        quest_id = self.db.create_quest(
            user_id=self.user_id,
            title=name,
            description=description,
            quest_type=quest_type,
            created_by=created_by,
            parent_quest_id=parent_quest_id
        )

        return quest_id

    def start_quest(self, quest_id: int) -> bool:
        """
        开始任务（状态：待开始 → 进行中）

        Args:
            quest_id: 任务ID

        Returns:
            bool: 是否成功
        """
        quest = self.db.get_quest(quest_id)
        if not quest:
            return False

        # 只有待开始状态才能开始
        if quest['status'] != 'pending':
            return False

        return self.db.update_quest_status(quest_id, 'in_progress')

    def complete_quest(
        self,
        quest_id: int,
        summary: str = "",
        xp_awarded: int = 0,
        attributes_awarded: Optional[Dict[str, int]] = None,
        ai_feedback: str = ""
    ) -> Dict:
        """
        完成任务

        Args:
            quest_id: 任务ID
            summary: 完成心得
            xp_awarded: 奖励经验值
            attributes_awarded: 奖励属性点
            ai_feedback: AI 评价

        Returns:
            Dict: {
                "success": bool,
                "completion_id": int,
                "xp_awarded": int,
                "attributes_awarded": dict
            }
        """
        quest = self.db.get_quest(quest_id)
        if not quest:
            return {"success": False, "error": "任务不存在"}

        # 只有进行中的任务才能完成
        if quest['status'] != 'in_progress':
            return {"success": False, "error": "任务未在进行中"}

        # 默认属性奖励
        if attributes_awarded is None:
            attributes_awarded = {}

        # 记录完成记录
        completion_id = self.db.complete_quest(
            quest_id=quest_id,
            user_id=self.user_id,
            summary=summary,
            xp_awarded=xp_awarded,
            attributes_awarded=attributes_awarded,
            ai_feedback=ai_feedback
        )

        if completion_id == 0:
            return {"success": False, "error": "完成记录保存失败"}

        return {
            "success": True,
            "completion_id": completion_id,
            "xp_awarded": xp_awarded,
            "attributes_awarded": attributes_awarded
        }

    def abandon_quest(self, quest_id: int) -> bool:
        """
        放弃任务

        Args:
            quest_id: 任务ID

        Returns:
            bool: 是否成功
        """
        quest = self.db.get_quest(quest_id)
        if not quest:
            return False

        # 只有待开始或进行中的任务才能放弃
        if quest['status'] not in ['pending', 'in_progress']:
            return False

        return self.db.update_quest_status(quest_id, 'abandoned')

    def get_quest(self, quest_id: int) -> Optional[Dict]:
        """
        获取任务详情

        Args:
            quest_id: 任务ID

        Returns:
            Dict: 任务信息
        """
        return self.db.get_quest(quest_id)

    def get_active_quests(
        self,
        quest_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """
        获取活跃任务列表

        Args:
            quest_type: 任务类型筛选
            quest_type: 任务状态筛选

        Returns:
            List[Dict]: 任务列表
        """
        return self.db.get_quests(
            user_id=self.user_id,
            quest_type=quest_type,
            status=status
        )

    def get_quests_by_type(self, quest_type: str) -> List[Dict]:
        """
        按类型获取任务

        Args:
            quest_type: 任务类型 (main/side/daily)

        Returns:
            List[Dict]: 任务列表
        """
        return self.get_active_quests(quest_type=quest_type)

    def get_in_progress_quests(self) -> List[Dict]:
        """
        获取进行中的任务

        Returns:
            List[Dict]: 任务列表
        """
        return self.get_active_quests(status='in_progress')

    def get_pending_quests(self) -> List[Dict]:
        """
        获取待开始的任务

        Returns:
            List[Dict]: 任务列表
        """
        return self.get_active_quests(status='pending')

    def get_completed_quests(self, limit: int = 10) -> List[Dict]:
        """
        获取已完成的任务

        Args:
            limit: 返回数量限制

        Returns:
            List[Dict]: 任务列表
        """
        return self.db.get_quests(
            user_id=self.user_id,
            status='completed',
            limit=limit
        )

    def get_subtasks(self, parent_quest_id: int) -> List[Dict]:
        """
        获取子任务列表

        Args:
            parent_quest_id: 父任务ID

        Returns:
            List[Dict]: 子任务列表
        """
        all_quests = self.db.get_quests(user_id=self.user_id)
        return [q for q in all_quests if q.get('parent_quest_id') == parent_quest_id]

    def get_quest_summary(self, quest_id: int) -> Optional[Dict]:
        """
        获取任务的完成心得

        Args:
            quest_id: 任务ID

        Returns:
            Dict: 完成记录，包含 summary, xp_awarded, attributes_awarded 等
        """
        quest = self.db.get_quest(quest_id)
        if not quest or quest['status'] != 'completed':
            return None

        # 从 quest_completion 表获取完成记录
        # 注意：需要在 DatabaseManager 中添加相应方法
        return self.db.get_quest_completion(quest_id)

    def get_quest_stats(self) -> Dict:
        """
        获取任务统计信息

        Returns:
            Dict: 统计数据
        """
        all_quests = self.db.get_quests(user_id=self.user_id)

        stats = {
            "total": len(all_quests),
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "abandoned": 0,
            "by_type": {
                "main": 0,
                "side": 0,
                "daily": 0
            }
        }

        for quest in all_quests:
            status = quest['status']
            quest_type = quest['type']

            stats[status] = stats.get(status, 0) + 1
            stats['by_type'][quest_type] = stats['by_type'].get(quest_type, 0) + 1

        return stats

    def update_quest(
        self,
        quest_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        quest_type: Optional[str] = None
    ) -> bool:
        """
        更新任务信息

        Args:
            quest_id: 任务ID
            name: 新名称
            description: 新描述
            quest_type: 新类型

        Returns:
            bool: 是否成功
        """
        quest = self.db.get_quest(quest_id)
        if not quest:
            return False

        # 构建更新字段
        updates = {}
        if name is not None:
            updates['name'] = name
        if description is not None:
            updates['description'] = description
        if quest_type is not None and quest_type in QUEST_TYPES:
            updates['quest_type'] = quest_type

        if not updates:
            return True  # 无需更新

        return self.db.update_quest(quest_id, updates)

    def can_start(self, quest_id: int) -> bool:
        """
        检查任务是否可以开始

        Args:
            quest_id: 任务ID

        Returns:
            bool: 是否可以开始
        """
        quest = self.db.get_quest(quest_id)
        if not quest:
            return False
        return quest['status'] == 'pending'

    def can_complete(self, quest_id: int) -> bool:
        """
        检查任务是否可以完成

        Args:
            quest_id: 任务ID

        Returns:
            bool: 是否可以完成
        """
        quest = self.db.get_quest(quest_id)
        if not quest:
            return False
        return quest['status'] == 'in_progress'

    def can_abandon(self, quest_id: int) -> bool:
        """
        检查任务是否可以放弃

        Args:
            quest_id: 任务ID

        Returns:
            bool: 是否可以放弃
        """
        quest = self.db.get_quest(quest_id)
        if not quest:
            return False
        return quest['status'] in ['pending', 'in_progress']


# 测试代码
if __name__ == "__main__":
    from ..database.db_manager import DatabaseManager

    print("=" * 60)
    print("任务系统测试")
    print("=" * 60)

    # 创建数据库和任务管理器
    db = DatabaseManager("data/voyager_test.db")
    quest_mgr = Quest(db, user_id=1)

    print("\n【1. 创建任务】")
    quest_id = quest_mgr.create_quest(
        name="学习 Python 装饰器",
        description="深入理解装饰器的原理和使用场景",
        quest_type="main",
        created_by="user"
    )
    print(f"创建主线任务 ID: {quest_id}")

    # 创建子任务
    sub1 = quest_mgr.create_quest(
        name="阅读装饰器文档",
        description="查看官方文档和教程",
        quest_type="side",
        parent_quest_id=quest_id,
        created_by="ai"
    )
    sub2 = quest_mgr.create_quest(
        name="实践装饰器应用",
        description="写几个装饰器示例",
        quest_type="side",
        parent_quest_id=quest_id,
        created_by="ai"
    )
    print(f"创建子任务 ID: {sub1}, {sub2}")

    print("\n【2. 获取任务列表】")
    stats = quest_mgr.get_quest_stats()
    print(f"任务统计: {stats}")

    pending = quest_mgr.get_pending_quests()
    print(f"待开始任务: {len(pending)} 个")

    print("\n【3. 开始任务】")
    success = quest_mgr.start_quest(quest_id)
    print(f"开始任务 {quest_id}: {'✅ 成功' if success else '❌ 失败'}")

    in_progress = quest_mgr.get_in_progress_quests()
    print(f"进行中任务: {len(in_progress)} 个")
    for q in in_progress:
        print(f"  - {q['name']} (ID: {q['id']})")

    print("\n【4. 完成任务】")
    result = quest_mgr.complete_quest(
        quest_id=quest_id,
        summary="通过阅读文档和实践，理解了装饰器的工作原理，学会了使用 @wraps 保留元信息。",
        xp_awarded=120,
        attributes_awarded={"knowledge": 15, "perseverance": 10},
        ai_feedback="很棒！你对装饰器的理解很到位，继续加油！"
    )
    print(f"完成任务结果: {result}")

    print("\n【5. 获取子任务】")
    subtasks = quest_mgr.get_subtasks(quest_id)
    print(f"任务 {quest_id} 的子任务: {len(subtasks)} 个")
    for sub in subtasks:
        print(f"  - {sub['name']} (状态: {sub['status']})")

    print("\n【6. 获取已完成任务】")
    completed = quest_mgr.get_completed_quests()
    print(f"已完成任务: {len(completed)} 个")
    for q in completed:
        print(f"  - {q['name']} (完成时间: {q['updated_at']})")

    print("\n【7. 测试状态检查】")
    print(f"任务 {sub1} 可以开始: {quest_mgr.can_start(sub1)}")
    print(f"任务 {sub1} 可以完成: {quest_mgr.can_complete(sub1)}")
    print(f"任务 {sub1} 可以放弃: {quest_mgr.can_abandon(sub1)}")

    print("\n【8. 放弃任务】")
    success = quest_mgr.abandon_quest(sub2)
    print(f"放弃任务 {sub2}: {'✅ 成功' if success else '❌ 失败'}")

    print("\n【9. 最终统计】")
    final_stats = quest_mgr.get_quest_stats()
    print(f"任务统计: {final_stats}")

    print("\n" + "=" * 60)
    print("✅ 任务系统测试完成！")
    print("=" * 60)
