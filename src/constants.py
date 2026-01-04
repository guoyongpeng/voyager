"""
启航者 (Voyager) - 常量定义
定义应用中使用的所有常量
"""

# ==================== 五维属性 ====================
ATTRIBUTES = {
    'knowledge': '知识',
    'expression': '表达',
    'empathy': '共情',
    'perseverance': '毅力',
    'courage': '勇气'
}

ATTRIBUTE_KEYS = list(ATTRIBUTES.keys())
ATTRIBUTE_NAMES = list(ATTRIBUTES.values())

# ==================== 任务类型 ====================
QUEST_TYPES = {
    'main': '主线',
    'side': '支线',
    'daily': '每日'
}

# ==================== 任务状态 ====================
QUEST_STATUS = {
    'pending': '待开始',
    'in_progress': '进行中',
    'completed': '已完成',
    'abandoned': '已放弃'
}

# ==================== 愿望状态 ====================
WISH_STATUS = {
    'locked': '锁定',
    'unlocked': '解锁',
    'achieved': '已实现'
}

# ==================== 经验值配置 ====================
XP_CONFIG = {
    'base_xp': 100,           # 基础经验值（升级到下一级所需）
    'multiplier': 1.5,        # 经验值增长倍数（指数曲线）
    'curve_type': 'exponential'  # 曲线类型：exponential（指数）或 linear（线性）
}

# ==================== 奖励配置 ====================
REWARD_CONFIG = {
    'base_xp': 50,            # 完成任务的基础经验奖励
    'max_bonus_xp': 100,      # 最大额外经验奖励
    'min_attribute_points': 5,    # 最小属性点奖励
    'max_attribute_points': 20,   # 最大属性点奖励
    'words_per_xp': 10        # 每多少字增加1点XP
}

# ==================== 成就类别 ====================
ACHIEVEMENT_CATEGORIES = {
    'quest': '任务',
    'attribute': '属性',
    'milestone': '里程碑'
}

# ==================== 数据库配置 ====================
DB_CONFIG = {
    'db_path': 'data/voyager.db',
    'migrations_path': 'src/database/migrations'
}

# ==================== 配置文件路径 ====================
CONFIG_PATH = 'data/config.json'

# ==================== UI 配置 ====================
UI_CONFIG = {
    'window_width': 1200,
    'window_height': 800,
    'kai_sphere_size': 80,
    'animation_duration': 2000,  # 毫秒
    'theme_colors': {
        'primary': '#64B5F6',    # 蓝色
        'secondary': '#81C784',  # 绿色
        'background': '#FAFAFA', # 浅灰
        'text': '#212121'        # 深灰
    }
}
