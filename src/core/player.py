"""
玩家系统 - 管理等级、经验值和五维属性
"""

import math
from typing import Dict
from ..database.db_manager import DatabaseManager
from ..constants import XP_CONFIG, ATTRIBUTES


class Player:
    """玩家系统，负责等级、经验、属性管理"""

    def __init__(self, db_manager: DatabaseManager, user_id: int = 1):
        """
        初始化玩家系统

        Args:
            db_manager: 数据库管理器实例
            user_id: 用户ID，默认为1
        """
        self.db = db_manager
        self.user_id = user_id

        # 经验值配置
        self.base_xp = XP_CONFIG['base_xp']
        self.multiplier = XP_CONFIG['multiplier']
        self.curve_type = XP_CONFIG['curve_type']

        # 从数据库加载数据
        self._load_data()

    def _load_data(self):
        """从数据库加载玩家数据"""
        user = self.db.get_user(self.user_id)

        if not user:
            raise ValueError(f"用户 ID {self.user_id} 不存在")

        self.level = user['level']
        self.current_xp = user['current_xp']
        self.total_xp = user['total_xp']

        # 加载属性
        attrs = self.db.get_attributes(self.user_id)
        self.attributes = {
            'knowledge': attrs.get('knowledge', 0),
            'expression': attrs.get('expression', 0),
            'empathy': attrs.get('empathy', 0),
            'perseverance': attrs.get('perseverance', 0),
            'courage': attrs.get('courage', 0)
        }

    def calculate_xp_for_level(self, level: int) -> int:
        """
        计算升到指定等级所需的累计经验值

        Args:
            level: 目标等级

        Returns:
            int: 所需经验值
        """
        if self.curve_type == "exponential":
            # 指数曲线：XP = BASE * (MULTIPLIER ^ (level - 1))
            return int(self.base_xp * math.pow(self.multiplier, level - 1))
        else:
            # 线性曲线：XP = BASE * level
            return self.base_xp * level

    def get_xp_to_next_level(self) -> int:
        """
        获取升到下一级还需要多少经验

        Returns:
            int: 所需经验值
        """
        return self.calculate_xp_for_level(self.level + 1) - self.current_xp

    def get_progress_to_next_level(self) -> float:
        """
        获取当前等级的进度（0-1）

        Returns:
            float: 进度百分比
        """
        xp_needed = self.calculate_xp_for_level(self.level + 1)
        if xp_needed == 0:
            return 1.0
        return min(1.0, self.current_xp / xp_needed)

    def add_xp(self, xp: int) -> Dict:
        """
        增加经验值，自动处理升级

        Args:
            xp: 要增加的经验值

        Returns:
            Dict: {
                "level_up": bool,  # 是否升级
                "new_level": int,  # 新等级
                "levels_gained": int,  # 升了几级
                "xp_to_next_level": int,  # 到下一级的经验
                "rewards": dict  # 升级奖励
            }
        """
        self.current_xp += xp
        self.total_xp += xp

        result = {
            "level_up": False,
            "new_level": self.level,
            "levels_gained": 0,
            "xp_to_next_level": 0,
            "rewards": {}
        }

        # 检查是否升级（可能连续升多级）
        while True:
            xp_needed = self.calculate_xp_for_level(self.level + 1)

            if self.current_xp >= xp_needed:
                # 升级！
                self.level += 1
                self.current_xp -= xp_needed
                result["level_up"] = True
                result["levels_gained"] += 1
                result["new_level"] = self.level

                # 升级奖励（每升一级获得5点可自由分配的属性点）
                # 这里暂时不自动分配，可以在 UI 中让用户选择
                if "attribute_points" not in result["rewards"]:
                    result["rewards"]["attribute_points"] = 0
                result["rewards"]["attribute_points"] += 5
            else:
                break

        result["xp_to_next_level"] = self.get_xp_to_next_level()

        # 保存到数据库
        self.db.update_user_xp(
            self.user_id,
            self.level,
            self.current_xp,
            self.total_xp
        )

        return result

    def get_attributes(self) -> Dict[str, int]:
        """
        获取当前属性

        Returns:
            Dict: 属性字典
        """
        return self.attributes.copy()

    def add_attributes(self, points: Dict[str, int]):
        """
        增加属性点

        Args:
            points: 要增加的属性点，如 {"knowledge": 10, "courage": 5}
        """
        for attr, value in points.items():
            if attr in self.attributes:
                self.attributes[attr] += value

        # 保存到数据库
        self.db.update_attributes(self.user_id, self.attributes)

    def get_total_attribute_points(self) -> int:
        """
        获取总属性点数

        Returns:
            int: 总属性点
        """
        return sum(self.attributes.values())

    def get_attribute_distribution(self) -> Dict[str, float]:
        """
        获取属性分布（百分比）

        Returns:
            Dict: 属性分布字典
        """
        total = self.get_total_attribute_points()
        if total == 0:
            return {attr: 0.0 for attr in self.attributes.keys()}

        return {
            attr: (value / total) * 100
            for attr, value in self.attributes.items()
        }

    def get_player_info(self) -> Dict:
        """
        获取完整的玩家信息

        Returns:
            Dict: 玩家信息字典
        """
        return {
            "user_id": self.user_id,
            "level": self.level,
            "current_xp": self.current_xp,
            "total_xp": self.total_xp,
            "xp_to_next_level": self.get_xp_to_next_level(),
            "progress": self.get_progress_to_next_level(),
            "attributes": self.attributes,
            "total_attribute_points": self.get_total_attribute_points()
        }

    def get_level_info(self) -> str:
        """
        获取等级信息的文字描述

        Returns:
            str: 等级描述
        """
        progress_percent = int(self.get_progress_to_next_level() * 100)
        return (
            f"Lv.{self.level} "
            f"({self.current_xp}/{self.calculate_xp_for_level(self.level + 1)} XP, "
            f"{progress_percent}%)"
        )

    def get_attribute_summary(self) -> str:
        """
        获取属性总结的文字描述

        Returns:
            str: 属性描述
        """
        parts = []
        for attr_key, attr_name in ATTRIBUTES.items():
            value = self.attributes.get(attr_key, 0)
            parts.append(f"{attr_name}: {value}")

        return " | ".join(parts)

    def refresh(self):
        """刷新玩家数据（从数据库重新加载）"""
        self._load_data()


# 测试代码
if __name__ == "__main__":
    from ..database.db_manager import DatabaseManager

    print("=" * 60)
    print("玩家系统测试")
    print("=" * 60)

    # 创建数据库和玩家
    db = DatabaseManager("data/voyager_test.db")
    player = Player(db, user_id=1)

    print("\n【1. 初始状态】")
    print(f"等级信息: {player.get_level_info()}")
    print(f"属性总结: {player.get_attribute_summary()}")

    print("\n【2. 测试增加经验】")
    result = player.add_xp(80)
    print(f"增加 80 XP")
    print(f"是否升级: {result['level_up']}")
    print(f"新等级: {result['new_level']}")
    print(f"到下一级: {result['xp_to_next_level']} XP")

    print("\n【3. 测试连续升级】")
    result = player.add_xp(500)
    print(f"增加 500 XP")
    print(f"升了几级: {result['levels_gained']}")
    print(f"当前等级: {player.level}")
    print(f"奖励: {result['rewards']}")

    print("\n【4. 测试增加属性】")
    player.add_attributes({'knowledge': 20, 'courage': 15})
    print(f"增加属性后: {player.get_attribute_summary()}")
    print(f"总属性点: {player.get_total_attribute_points()}")

    print("\n【5. 完整信息】")
    info = player.get_player_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ 玩家系统测试完成！")
    print("=" * 60)
