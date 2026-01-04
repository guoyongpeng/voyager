"""
数据库管理器 - SQLite 数据访问层
提供所有数据库操作的统一接口
"""

import sqlite3
import json
import os
from typing import Dict, List, Optional, Tuple
from contextlib import contextmanager
from datetime import datetime, date


class DatabaseManager:
    """SQLite 数据库管理器"""

    def __init__(self, db_path: str = "data/voyager.db"):
        """
        初始化数据库管理器

        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path

        # 确保 data 目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # 初始化数据库
        self.init_database()

    @contextmanager
    def get_connection(self):
        """
        上下文管理器，自动管理数据库连接

        Yields:
            sqlite3.Connection: 数据库连接对象
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 返回字典形式的行
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_database(self):
        """初始化数据库（执行建表脚本）"""
        # 读取 SQL 初始化脚本
        sql_file = os.path.join(
            os.path.dirname(__file__),
            "migrations",
            "init_db.sql"
        )

        if not os.path.exists(sql_file):
            raise FileNotFoundError(f"SQL 初始化脚本不存在: {sql_file}")

        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # 执行脚本
        with self.get_connection() as conn:
            conn.executescript(sql_script)

    # ==================== 用户相关 ====================

    def get_user(self, user_id: int = 1) -> Optional[Dict]:
        """
        获取用户信息

        Args:
            user_id: 用户ID，默认为1（单用户）

        Returns:
            Dict: 用户信息字典，如果不存在返回 None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def create_user(self, username: str) -> int:
        """
        创建新用户

        Args:
            username: 用户名

        Returns:
            int: 新用户的ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user (username) VALUES (?)",
                (username,)
            )
            user_id = cursor.lastrowid

            # 同时创建属性记录
            cursor.execute(
                "INSERT INTO attributes (user_id) VALUES (?)",
                (user_id,)
            )

            return user_id

    def update_user_xp(
        self,
        user_id: int,
        level: int,
        current_xp: int,
        total_xp: int
    ):
        """
        更新用户经验值和等级

        Args:
            user_id: 用户ID
            level: 新等级
            current_xp: 当前等级经验
            total_xp: 总经验值
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user
                SET level = ?, current_xp = ?, total_xp = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (level, current_xp, total_xp, user_id))

    # ==================== 属性相关 ====================

    def get_attributes(self, user_id: int = 1) -> Dict:
        """
        获取用户属性

        Args:
            user_id: 用户ID

        Returns:
            Dict: 属性字典
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM attributes WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else {}

    def update_attributes(self, user_id: int, attributes: Dict[str, int]):
        """
        更新用户属性

        Args:
            user_id: 用户ID
            attributes: 属性字典，如 {"knowledge": 50, "courage": 30}
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE attributes
                SET knowledge = ?, expression = ?, empathy = ?,
                    perseverance = ?, courage = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (
                attributes.get('knowledge', 0),
                attributes.get('expression', 0),
                attributes.get('empathy', 0),
                attributes.get('perseverance', 0),
                attributes.get('courage', 0),
                user_id
            ))

    def add_attribute_points(self, user_id: int, points: Dict[str, int]):
        """
        增加属性点（在现有基础上增加）

        Args:
            user_id: 用户ID
            points: 要增加的属性点，如 {"knowledge": 10, "courage": 5}
        """
        current = self.get_attributes(user_id)

        new_attributes = {
            'knowledge': current.get('knowledge', 0) + points.get('knowledge', 0),
            'expression': current.get('expression', 0) + points.get('expression', 0),
            'empathy': current.get('empathy', 0) + points.get('empathy', 0),
            'perseverance': current.get('perseverance', 0) + points.get('perseverance', 0),
            'courage': current.get('courage', 0) + points.get('courage', 0)
        }

        self.update_attributes(user_id, new_attributes)

    # ==================== 任务相关 ====================

    def create_quest(
        self,
        user_id: int,
        title: str,
        description: str = "",
        quest_type: str = 'side',
        created_by: str = 'user',
        priority: int = 0,
        deadline: Optional[str] = None,
        parent_quest_id: Optional[int] = None
    ) -> int:
        """
        创建新任务

        Args:
            user_id: 用户ID
            title: 任务标题
            description: 任务描述
            quest_type: 任务类型 (main/side/daily)
            created_by: 创建者 (user/ai)
            priority: 优先级
            deadline: 截止时间
            parent_quest_id: 父任务ID（子任务时使用）

        Returns:
            int: 新任务的ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO quest
                (user_id, title, description, type, created_by, priority, deadline, parent_quest_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, title, description, quest_type, created_by, priority, deadline, parent_quest_id))
            return cursor.lastrowid

    def get_quest(self, quest_id: int) -> Optional[Dict]:
        """获取单个任务"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM quest WHERE id = ?", (quest_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_quests(
        self,
        user_id: int = 1,
        status: Optional[str] = None,
        quest_type: Optional[str] = None
    ) -> List[Dict]:
        """
        获取任务列表

        Args:
            user_id: 用户ID
            status: 状态过滤 (pending/in_progress/completed/abandoned)
            quest_type: 类型过滤 (main/side/daily)

        Returns:
            List[Dict]: 任务列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM quest WHERE user_id = ?"
            params = [user_id]

            if status:
                query += " AND status = ?"
                params.append(status)

            if quest_type:
                query += " AND type = ?"
                params.append(quest_type)

            query += " ORDER BY priority DESC, created_at DESC"

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def update_quest_status(
        self,
        quest_id: int,
        status: str,
        timestamp_field: Optional[str] = None
    ):
        """
        更新任务状态

        Args:
            quest_id: 任务ID
            status: 新状态
            timestamp_field: 要更新的时间戳字段 (started_at/completed_at)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            if timestamp_field:
                cursor.execute(f"""
                    UPDATE quest
                    SET status = ?, {timestamp_field} = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (status, quest_id))
            else:
                cursor.execute(
                    "UPDATE quest SET status = ? WHERE id = ?",
                    (status, quest_id)
                )

    def complete_quest(
        self,
        quest_id: int,
        user_id: int,
        summary: str,
        xp_awarded: int,
        attributes_awarded: Dict[str, int],
        ai_feedback: str
    ) -> int:
        """
        完成任务并记录

        Args:
            quest_id: 任务ID
            user_id: 用户ID
            summary: 用户心得
            xp_awarded: 奖励经验值
            attributes_awarded: 奖励属性点
            ai_feedback: AI 评语

        Returns:
            int: 完成记录ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. 更新任务状态
            cursor.execute("""
                UPDATE quest
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (quest_id,))

            # 2. 创建完成记录
            cursor.execute("""
                INSERT INTO quest_completion
                (quest_id, user_id, summary, xp_awarded, attributes_awarded, ai_feedback)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                quest_id,
                user_id,
                summary,
                xp_awarded,
                json.dumps(attributes_awarded),
                ai_feedback
            ))

            return cursor.lastrowid

    def get_quest_completion(self, quest_id: int) -> Optional[Dict]:
        """
        获取任务完成记录

        Args:
            quest_id: 任务ID

        Returns:
            Dict: 完成记录，包含 summary, xp_awarded, attributes_awarded 等
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM quest_completion
                WHERE quest_id = ?
                ORDER BY completed_at DESC
                LIMIT 1
            """, (quest_id,))
            row = cursor.fetchone()
            if row:
                result = dict(row)
                # 解析 JSON 字段
                if result.get('attributes_awarded'):
                    result['attributes_awarded'] = json.loads(result['attributes_awarded'])
                return result
            return None

    def delete_quest(self, quest_id: int):
        """删除任务"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM quest WHERE id = ?", (quest_id,))

    # ==================== 愿望相关 ====================

    def create_wish(
        self,
        user_id: int,
        title: str,
        description: str = "",
        unlock_level: int = 1
    ) -> int:
        """创建愿望"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO wish (user_id, title, description, unlock_level)
                VALUES (?, ?, ?, ?)
            """, (user_id, title, description, unlock_level))
            return cursor.lastrowid

    def get_wishes(self, user_id: int = 1) -> List[Dict]:
        """获取愿望列表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM wish WHERE user_id = ? ORDER BY unlock_level",
                (user_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def unlock_wish(self, wish_id: int):
        """解锁愿望"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE wish SET status = 'unlocked' WHERE id = ?",
                (wish_id,)
            )

    # ==================== 成就相关 ====================

    def get_achievements(self) -> List[Dict]:
        """获取所有成就"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM achievement")
            return [dict(row) for row in cursor.fetchall()]

    def unlock_achievement(self, user_id: int, achievement_id: int):
        """解锁成就"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO user_achievement (user_id, achievement_id)
                    VALUES (?, ?)
                """, (user_id, achievement_id))
            except sqlite3.IntegrityError:
                # 已经解锁过了，忽略
                pass

    def get_user_achievements(self, user_id: int = 1) -> List[Dict]:
        """获取用户已解锁的成就"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.*, ua.unlocked_at
                FROM achievement a
                JOIN user_achievement ua ON a.id = ua.achievement_id
                WHERE ua.user_id = ?
                ORDER BY ua.unlocked_at DESC
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]

    # ==================== 对话历史 ====================

    def save_chat_message(
        self,
        user_id: int,
        role: str,
        content: str,
        session_id: Optional[str] = None
    ):
        """保存对话消息"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chat_history (user_id, role, content, session_id)
                VALUES (?, ?, ?, ?)
            """, (user_id, role, content, session_id))

    def get_chat_history(
        self,
        user_id: int = 1,
        session_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """获取对话历史"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            if session_id:
                cursor.execute("""
                    SELECT * FROM chat_history
                    WHERE user_id = ? AND session_id = ?
                    ORDER BY created_at DESC LIMIT ?
                """, (user_id, session_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM chat_history
                    WHERE user_id = ?
                    ORDER BY created_at DESC LIMIT ?
                """, (user_id, limit))

            return [dict(row) for row in cursor.fetchall()]

    # ==================== 统计数据 ====================

    def record_daily_stats(
        self,
        user_id: int,
        quests_completed: int,
        xp_gained: int,
        attributes_gained: Dict[str, int]
    ):
        """记录每日统计"""
        today = date.today().isoformat()

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO statistics
                (user_id, date, quests_completed, xp_gained, attributes_gained)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, date) DO UPDATE SET
                    quests_completed = quests_completed + ?,
                    xp_gained = xp_gained + ?,
                    attributes_gained = ?
            """, (
                user_id,
                today,
                quests_completed,
                xp_gained,
                json.dumps(attributes_gained),
                quests_completed,
                xp_gained,
                json.dumps(attributes_gained)
            ))

    def get_statistics(
        self,
        user_id: int = 1,
        days: int = 7
    ) -> List[Dict]:
        """获取统计数据"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM statistics
                WHERE user_id = ?
                ORDER BY date DESC LIMIT ?
            """, (user_id, days))
            return [dict(row) for row in cursor.fetchall()]


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("数据库管理器测试")
    print("=" * 60)

    # 创建数据库管理器
    db = DatabaseManager("data/voyager_test.db")

    # 测试用户操作
    print("\n【1. 测试用户操作】")
    user = db.get_user(1)
    print(f"用户信息: {user}")

    # 测试属性操作
    print("\n【2. 测试属性操作】")
    attrs = db.get_attributes(1)
    print(f"当前属性: {attrs}")

    db.add_attribute_points(1, {'knowledge': 10, 'courage': 5})
    attrs = db.get_attributes(1)
    print(f"增加后属性: {attrs}")

    # 测试任务操作
    print("\n【3. 测试任务操作】")
    quest_id = db.create_quest(
        user_id=1,
        title="测试任务：学习数据库",
        description="掌握 SQLite 基本操作",
        quest_type='side'
    )
    print(f"创建任务 ID: {quest_id}")

    quests = db.get_quests(1, status='pending')
    print(f"待开始任务数: {len(quests)}")

    # 测试完成任务
    print("\n【4. 测试完成任务】")
    completion_id = db.complete_quest(
        quest_id=quest_id,
        user_id=1,
        summary="学习了 SQLite 的基本操作，理解了数据库设计",
        xp_awarded=80,
        attributes_awarded={'knowledge': 15},
        ai_feedback="掌握得很好！继续加油！"
    )
    print(f"完成记录 ID: {completion_id}")

    # 测试更新经验值
    print("\n【5. 测试更新经验值】")
    db.update_user_xp(1, level=2, current_xp=30, total_xp=130)
    user = db.get_user(1)
    print(f"更新后用户: Level {user['level']}, XP: {user['total_xp']}")

    print("\n" + "=" * 60)
    print("✅ 数据库管理器测试完成！")
    print("=" * 60)
