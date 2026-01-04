-- 启航者 (Voyager) 数据库初始化脚本
-- SQLite 数据库结构定义

-- 用户表（单用户，但预留多用户扩展）
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    level INTEGER DEFAULT 1,
    current_xp INTEGER DEFAULT 0,
    total_xp INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 五维属性表
CREATE TABLE IF NOT EXISTS attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    knowledge INTEGER DEFAULT 0,      -- 知识
    expression INTEGER DEFAULT 0,     -- 表达
    empathy INTEGER DEFAULT 0,        -- 共情
    perseverance INTEGER DEFAULT 0,   -- 毅力
    courage INTEGER DEFAULT 0,        -- 勇气
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 任务表
CREATE TABLE IF NOT EXISTS quest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    type TEXT CHECK(type IN ('main', 'side', 'daily')) DEFAULT 'side',
    status TEXT CHECK(status IN ('pending', 'in_progress', 'completed', 'abandoned')) DEFAULT 'pending',
    priority INTEGER DEFAULT 0,
    created_by TEXT CHECK(created_by IN ('user', 'ai')) DEFAULT 'user',
    parent_quest_id INTEGER,          -- 父任务ID（子任务时使用）
    ai_context TEXT,                  -- AI 创建任务时的上下文
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    deadline TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (parent_quest_id) REFERENCES quest(id)
);

-- 任务完成记录（用于奖励计算和历史追踪）
CREATE TABLE IF NOT EXISTS quest_completion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quest_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    summary TEXT,                     -- 用户心得体会
    xp_awarded INTEGER DEFAULT 0,
    attributes_awarded TEXT,          -- JSON 格式存储属性奖励
    ai_feedback TEXT,                 -- AI 评语
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quest_id) REFERENCES quest(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 愿望表
CREATE TABLE IF NOT EXISTS wish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    unlock_level INTEGER DEFAULT 1,   -- 解锁等级
    status TEXT CHECK(status IN ('locked', 'unlocked', 'achieved')) DEFAULT 'locked',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    achieved_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 成就表
CREATE TABLE IF NOT EXISTS achievement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,        -- 成就代码（如 'first_quest'）
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT,                        -- 图标路径
    category TEXT,                    -- 分类（如 '任务', '属性', '里程碑'）
    requirement TEXT                  -- JSON 格式的解锁条件
);

-- 用户成就关联表
CREATE TABLE IF NOT EXISTS user_achievement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (achievement_id) REFERENCES achievement(id),
    UNIQUE(user_id, achievement_id)
);

-- 对话历史表（用于 AI 上下文和分析）
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role TEXT CHECK(role IN ('user', 'assistant')) NOT NULL,
    content TEXT NOT NULL,
    session_id TEXT,                  -- 会话 ID（用于区分不同对话会话）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 统计数据表（用于可视化）
CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    quests_completed INTEGER DEFAULT 0,
    xp_gained INTEGER DEFAULT 0,
    attributes_gained TEXT,           -- JSON 格式
    FOREIGN KEY (user_id) REFERENCES user(id),
    UNIQUE(user_id, date)
);

-- 索引优化
CREATE INDEX IF NOT EXISTS idx_quest_user_status ON quest(user_id, status);
CREATE INDEX IF NOT EXISTS idx_quest_completion_user ON quest_completion(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_session ON chat_history(session_id);
CREATE INDEX IF NOT EXISTS idx_statistics_date ON statistics(user_id, date);

-- 插入默认用户数据
INSERT OR IGNORE INTO user (id, username) VALUES (1, 'voyager');
INSERT OR IGNORE INTO attributes (user_id, knowledge, expression, empathy, perseverance, courage)
VALUES (1, 0, 0, 0, 0, 0);

-- 插入预置成就
INSERT OR IGNORE INTO achievement (code, name, description, category, requirement) VALUES
('first_quest', '初次启航', '完成第一个任务', '任务', '{"type": "quest_count", "count": 1}'),
('persistent_week', '坚持不懈', '连续7天完成任务', '里程碑', '{"type": "consecutive_days", "days": 7}'),
('all_round', '全能发展', '五维属性均达到50', '属性', '{"type": "all_attributes", "min": 50}'),
('knowledge_master', '知识大师', '知识属性达到100', '属性', '{"type": "attribute", "name": "knowledge", "value": 100}'),
('brave_heart', '勇者之心', '勇气属性达到100', '属性', '{"type": "attribute", "name": "courage", "value": 100}'),
('level_10', '十级冒险者', '达到10级', '里程碑', '{"type": "level", "value": 10}'),
('level_20', '二十级英雄', '达到20级', '里程碑', '{"type": "level", "value": 20}'),
('quest_master', '任务大师', '完成100个任务', '任务', '{"type": "quest_count", "count": 100}');
