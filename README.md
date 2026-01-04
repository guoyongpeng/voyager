# 启航者 (Voyager)

**一个以本地规则引擎为核心的个人成长游戏化应用**

> 完全本地化 | 隐私优先 | 离线可用 | AI 可选增强

---

## 📖 项目概述

启航者 (Voyager) 是一个将个人成长过程游戏化的桌面应用，通过任务管理、经验值系统和五维属性培养，帮助用户持续自我提升。

### 核心特点

✅ **完全本地化** - 所有核心功能基于本地规则引擎，无需任何 API
✅ **隐私优先** - 数据完全本地存储（SQLite），不上传云端
✅ **离线可用** - 无网络环境下也能正常使用
✅ **AI 可选** - 用户可选配置智谱 AI 获得更智能的体验
✅ **游戏化** - 等级、经验值、五维属性、成就系统

---

## 🎮 功能特性

### 1. AI 助手"凯"（本地规则引擎）

- **任务拆解** - 基于 8+ 类别模板，将大目标分解为可执行子任务
- **情绪检测** - 通过关键词识别情绪，主动推荐放松/整理类任务
- **任务建议** - 预设 10+ 类别建议库，提供执行指导
- **奖励评判** - 基于关键词和规则计算经验值和属性点

### 2. 成长系统

- **等级系统** - 指数型经验曲线（BASE: 100 XP，倍数: 1.5）
- **五维属性** - 知识、表达、共情、毅力、勇气
- **属性雷达图** - 可视化成长轨迹

### 3. 任务管理

- **任务类型** - 主线、支线、每日
- **任务状态** - 待开始、进行中、已完成、已放弃
- **心得记录** - 完成任务后记录心得，获得奖励

### 4. 愿望系统

- 长期目标管理
- 等级解锁机制

### 5. 成就系统

- 8+ 预置成就
- 自动检测触发

### 6. 数据统计

- 成长曲线可视化
- 每日/每周统计
- 数据导入/导出

---

## 🏗️ 技术架构

### 技术栈

- **UI 框架**: PyQt5 5.15.9
- **数据库**: SQLite3
- **数据可视化**: Matplotlib 3.7.2
- **AI 可选**: 智谱 GLM-4（可选）
- **加密**: Cryptography 41.0.3

### 目录结构

```
cc-yongzhe/
├── src/
│   ├── ai/                        # AI/智能服务层
│   │   ├── base_engine.py        # 引擎抽象基类
│   │   ├── local_engine.py       # 本地规则引擎【默认】
│   │   ├── kai.py                # "凯"助手统一接口
│   │   ├── dialogue_templates.py # 预设话术模板库
│   │   └── rule_based/           # 本地规则模块
│   │       ├── task_decomposer.py   # 任务拆解器
│   │       ├── emotion_detector.py  # 情绪检测器
│   │       ├── reward_calculator.py # 奖励计算器
│   │       └── suggestion_db.py     # 建议数据库
│   ├── core/                      # 核心业务逻辑
│   │   ├── player.py             # 玩家系统
│   │   └── quest.py              # 任务系统
│   ├── database/                  # 数据访问层
│   │   ├── db_manager.py         # 数据库管理器
│   │   └── migrations/
│   │       └── init_db.sql       # 数据库初始化脚本
│   ├── ui/                        # UI 组件层
│   │   ├── main_window.py        # 主窗口
│   │   └── widgets/              # 自定义组件
│   ├── utils/                     # 工具类
│   └── constants.py               # 常量定义
├── data/                          # 数据目录
│   ├── voyager.db                # SQLite 数据库
│   └── config.json               # 配置文件
├── docs/                          # 文档
│   ├── prd.md                    # 产品需求文档
│   └── ai-docs/prompt.md         # AI 提示词文档
└── requirements.txt               # Python 依赖
```

---

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 初始化数据库

```bash
python -c "from src.database.db_manager import DatabaseManager; DatabaseManager('data/voyager.db')"
```

### 测试本地规则引擎

```bash
# 测试奖励计算器
python src/ai/rule_based/reward_calculator.py

# 测试任务拆解器
python src/ai/rule_based/task_decomposer.py

# 测试情绪检测器
python src/ai/rule_based/emotion_detector.py

# 测试建议数据库
python src/ai/rule_based/suggestion_db.py

# 测试完整本地引擎
python src/ai/local_engine.py

# 测试 Kai 助手接口
python src/ai/kai.py
```

---

## 📊 数据库设计

### 核心表

- **user** - 用户表（等级、经验值）
- **attributes** - 五维属性表
- **quest** - 任务表
- **quest_completion** - 任务完成记录
- **wish** - 愿望表
- **achievement** - 成就表
- **user_achievement** - 用户成就关联表
- **chat_history** - 对话历史表
- **statistics** - 统计数据表

---

## 🎯 开发进度

### ✅ 已完成（70%）

- [x] 项目目录结构搭建
- [x] 数据库表结构设计（9张表 + 索引）
- [x] 常量定义（属性、配置、奖励等）
- [x] **本地规则引擎（核心）**
  - [x] 奖励计算器（关键词 → 属性点 + XP）
  - [x] 任务拆解器（8+ 类别模板）
  - [x] 情绪检测器（关键词匹配 + 任务推荐）
  - [x] 建议数据库（10+ 类别建议库）
- [x] 本地引擎整合（LocalEngine）
- [x] 对话模板库（问候、鼓励、庆祝等 50+ 条话术）
- [x] AI 助手"凯"统一接口

### 🚧 进行中（30%）

- [ ] 数据库管理器（DatabaseManager）
- [ ] 配置管理器（ConfigManager）
- [ ] 核心业务逻辑
  - [ ] Player 类（等级/经验/属性管理）
  - [ ] Quest 类（任务 CRUD）
- [ ] UI 界面
  - [ ] 主窗口框架
  - [ ] 玩家面板（等级、雷达图）
  - [ ] 任务面板
  - [ ] AI 对话窗口
- [ ] 应用入口（main.py）

### 📝 待实现

- [ ] AI 增强引擎（LLMEngine - 可选）
- [ ] 成就系统完整实现
- [ ] 数据统计可视化
- [ ] 数据导入/导出功能

---

## 🧪 测试示例

### 任务拆解测试

```python
from src.ai.kai import Kai

kai = Kai()

# 步骤1：获取引导问题
goal = "学习 Python 编程"
question = kai.decompose_task(goal)
print(question)
# 输出: "你想学习学习 Python 编程的哪个方面？（如基础概念、实践操作、进阶技巧等）"

# 步骤2：生成子任务
answer = "从基础语法开始"
subtasks = kai.decompose_task(goal, answer)
for task in subtasks:
    print(f"- {task['name']}: {task['description']}")
```

### 奖励计算测试

```python
from src.ai.kai import Kai

kai = Kai()

task_name = "学习 Python 列表操作"
summary = "今天学习了列表的添加、删除、切片等操作，通过查资料和实践理解了原理，坚持完成了练习。"

reward = kai.judge_completion(task_name, summary)
print(f"经验值: {reward['xp_awarded']} XP")
print(f"属性: {reward['attributes_awarded']}")
print(f"评语: {reward['feedback_text']}")
```

---

## 🤝 贡献指南

欢迎贡献！可以通过以下方式参与：

1. 扩展任务拆解模板（更多类别）
2. 丰富关键词词库（属性、情绪）
3. 增加对话话术模板
4. 优化奖励计算算法
5. UI 设计和实现

---

## 📄 许可证

MIT License

---

## 🙏 致谢

感谢所有为个人成长努力的你！

---

**启航者，让成长可见。**
