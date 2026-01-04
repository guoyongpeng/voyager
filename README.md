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
✅ **现代 UI** - PyQt5 实现，简约设计，流畅动画

---

## 🎮 功能特性

### 1. AI 助手"凯"（本地规则引擎）

- **任务拆解** - 基于 8+ 类别模板，将大目标分解为可执行子任务
- **情绪检测** - 通过关键词识别 5 种情绪，主动推荐放松/整理类任务
- **任务建议** - 预设 10+ 类别建议库，提供执行指导
- **奖励评判** - 基于关键词和规则计算经验值和属性点（5 属性 × 15+ 关键词）
- **对话交互** - 50+ 条预设话术，自然流畅的对话体验

### 2. 成长系统

- **等级系统** - 指数型经验曲线（BASE: 100 XP，倍数: 1.5）
- **五维属性** - 知识、表达、共情、毅力、勇气
- **属性雷达图** - 可视化成长轨迹，800ms 平滑动画过渡
- **升级奖励** - 每级获得 5 属性点自由分配

### 3. 任务管理

- **任务类型** - 主线、支线、每日
- **任务状态** - 待开始、进行中、已完成、已放弃
- **心得记录** - 完成任务后记录心得，AI 自动评判奖励
- **父子任务** - 支持任务拆解和关联

### 4. 精美 UI 界面

- **主窗口** - 左右分栏设计，玩家面板 + 任务面板
- **任务卡片** - 精美卡片式设计，悬停效果，右键菜单
- **凯悬浮球** - 呼吸动画（透明度 + 缩放，2秒循环）
- **对话窗口** - 气泡样式聊天界面，支持情绪检测
- **五维雷达图** - 正五边形可视化，平滑动画

### 5. 成就系统

- 8+ 预置成就（数据库已初始化）
- 自动检测触发机制

### 6. 数据统计

- 任务统计（总数、完成数、进行中）
- 经验值和等级追踪
- 属性成长记录

---

## 🏗️ 技术架构

### 技术栈

- **UI 框架**: PyQt5 5.15.9
- **数据库**: SQLite3
- **AI 可选**: 智谱 GLM-4（可选增强）
- **加密**: Cryptography 41.0.3（API Key 加密存储）
- **动画**: QPropertyAnimation（平滑过渡效果）

### 核心架构

```
用户 → "凯"助手接口 (kai.py)
          ↓
    检测 AI Key 配置
     /          \
 无配置          有配置
   ↓              ↓
LocalEngine    LLMEngine
（本地规则）    （智谱AI增强）
```

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
│   │       ├── task_decomposer.py   # 任务拆解器（8+ 类别）
│   │       ├── emotion_detector.py  # 情绪检测器（5 种情绪）
│   │       ├── reward_calculator.py # 奖励计算器
│   │       └── suggestion_db.py     # 建议数据库（10+ 类别）
│   ├── core/                      # 核心业务逻辑
│   │   ├── player.py             # 玩家系统（等级/经验/属性）
│   │   └── quest.py              # 任务系统（完整生命周期）
│   ├── database/                  # 数据访问层
│   │   ├── db_manager.py         # 数据库管理器（20+ CRUD 方法）
│   │   └── migrations/
│   │       └── init_db.sql       # 数据库初始化脚本（9张表）
│   ├── ui/                        # UI 组件层
│   │   ├── main_window.py        # 主窗口
│   │   ├── widgets/              # 自定义组件
│   │   │   ├── player_panel.py  # 玩家状态面板
│   │   │   ├── radar_chart.py   # 五维雷达图
│   │   │   ├── quest_card.py    # 任务卡片
│   │   │   ├── quest_panel.py   # 任务面板
│   │   │   └── kai_sphere.py    # 凯悬浮球
│   │   └── dialogs/              # 对话框
│   │       └── chat_dialog.py   # AI 对话窗口
│   ├── utils/                     # 工具类
│   │   └── crypto.py             # API Key 加密
│   ├── config.py                  # 配置管理器（单例）
│   └── constants.py               # 常量定义
├── tests/                         # 测试
│   ├── test_full_workflow.py     # 端到端测试（13 项功能）
│   └── create_test_data.py       # 测试数据生成
├── data/                          # 数据目录
│   ├── voyager.db                # SQLite 数据库
│   └── config.json               # 配置文件
├── docs/                          # 文档
│   ├── prd.md                    # 产品需求文档
│   └── ai-docs/prompt.md         # AI 提示词文档
├── main.py                        # 应用入口
├── requirements.txt               # Python 依赖
├── LICENSE                        # MIT 许可证
├── CONTRIBUTING.md                # 贡献指南
├── FINAL_SUMMARY.md               # 项目总结
└── CHANGELOG.md                   # 更新日志
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

**依赖清单：**
- PyQt5==5.15.9
- cryptography==41.0.3
- matplotlib==3.7.2（可选，用于数据可视化）

### 2. 创建测试数据

```bash
python tests/create_test_data.py
```

这将创建：
- 初始玩家数据（Lv.3，200 XP）
- 6 个示例任务
- 初始属性点分配

### 3. 运行应用

```bash
python main.py
```

### 4. 运行测试

```bash
python tests/test_full_workflow.py
```

测试覆盖 13 项核心功能：
- 系统初始化
- 任务拆解
- 任务创建
- 任务状态管理
- AI 建议
- 情绪检测
- 任务完成
- 奖励计算
- 玩家成长
- 统计查询

---

## 📊 数据库设计

### 核心表（9张表）

1. **user** - 用户表（id, username, level, current_xp, total_xp）
2. **attributes** - 五维属性表（knowledge, expression, empathy, perseverance, courage）
3. **quest** - 任务表（title, type, status, parent_quest_id）
4. **quest_completion** - 任务完成记录（summary, xp_awarded, attributes_awarded, ai_feedback）
5. **wish** - 愿望表（unlock_level, status）
6. **achievement** - 成就表（code, name, requirement）
7. **user_achievement** - 用户成就关联表
8. **chat_history** - 对话历史表（role, content, session_id）
9. **statistics** - 统计数据表（date, quests_completed, xp_gained）

**关系设计：**
- 外键约束确保数据完整性
- 索引优化查询性能
- 预置成就数据

---

## 🎯 开发进度

**总体完成度**: **90%** ✅

### ✅ 已完成

#### 核心系统（100% ✅）
- [x] 数据库设计（9张表 + 索引 + 预置数据）
- [x] DatabaseManager（20+ CRUD 方法）
- [x] ConfigManager（JSON 配置 + API Key 加密）
- [x] 常量定义（属性、配置、奖励等）

#### AI 本地规则引擎（100% ✅）
- [x] 奖励计算器（关键词 → 属性点 + XP）
- [x] 任务拆解器（8+ 类别模板）
- [x] 情绪检测器（5 种情绪 × 10+ 关键词）
- [x] 建议数据库（10+ 类别 × 7+ 建议）
- [x] 对话模板库（50+ 条话术）
- [x] 本地引擎整合（LocalEngine）
- [x] AI 助手"凯"统一接口

#### 业务逻辑层（100% ✅）
- [x] Player 类（等级/经验/属性管理）
- [x] Quest 类（任务完整生命周期）
- [x] 指数型经验曲线
- [x] 多级连续升级处理

#### UI 界面（95% ✅）
- [x] 主窗口框架（左右分栏布局）
- [x] 玩家面板（等级、经验条、雷达图）
- [x] 五维雷达图（800ms 平滑动画）
- [x] 任务卡片（精美设计 + 悬停效果）
- [x] 任务面板（筛选、新建、操作）
- [x] 凯悬浮球（呼吸动画）
- [x] AI 对话窗口（气泡样式）
- [x] 菜单栏和状态栏

#### 测试与工具（100% ✅）
- [x] 端到端测试（13 项功能全部通过）
- [x] 测试数据生成脚本
- [x] UTF-8 编码兼容（Windows）

### 🚧 待完成（10%）

- [ ] LLM 增强引擎（智谱 GLM-4 集成 - 可选）
- [ ] 任务拆解对话框（集成两步引导）
- [ ] 成就系统 UI 界面
- [ ] 数据可视化图表（matplotlib）
- [ ] 数据导入/导出功能

---

## 🧪 使用示例

### 1. 使用本地规则引擎

```python
from src.ai.kai import Kai

# 创建 AI 助手（自动使用本地引擎）
kai = Kai(config_manager=None)

# 任务拆解
goal = "学习 Python 编程"
question = kai.decompose_task(goal)
print(question)
# 输出: "你想学习学习 Python 编程的哪个方面？（如基础概念、实践操作、进阶技巧等）"

answer = "从基础语法开始"
subtasks = kai.decompose_task(goal, answer)
for task in subtasks:
    print(f"- {task['name']}: {task['description']}")

# 奖励评判
task_name = "学习 Python 列表操作"
summary = "今天学习了列表的添加、删除、切片等操作，通过查资料和实践理解了原理，坚持完成了练习。"

reward = kai.judge_completion(task_name, summary)
print(f"经验值: {reward['xp_awarded']} XP")
print(f"属性: {reward['attributes_awarded']}")
print(f"评语: {reward['feedback_text']}")

# 情绪检测
user_input = "今天好累，压力好大"
emotion = kai.analyze_emotion(user_input)
if emotion:
    print(f"检测到情绪: {emotion}")
    print(f"建议: {emotion['suggestion']}")
```

### 2. 运行完整应用

```bash
# 1. 创建测试数据
python tests/create_test_data.py

# 2. 启动应用
python main.py

# 3. 体验功能
# - 查看玩家面板（等级、经验、五维雷达图）
# - 创建任务（点击"新建任务"按钮）
# - 开始任务（右键菜单 → 开始任务）
# - 完成任务（右键菜单 → 完成任务 → 输入心得）
# - 与凯对话（点击右下角悬浮球）
```

---

## 🎨 UI 功能说明

### 主界面

- **左侧玩家面板**：
  - 等级显示（动态高亮）
  - 经验进度条（百分比）
  - 五维雷达图（平滑动画）
  - 属性详细列表

- **右侧任务面板**：
  - 筛选按钮（全部/待开始/进行中/已完成）
  - 新建任务按钮
  - 任务卡片列表
  - 右键菜单（开始/完成/放弃）

- **右下角凯悬浮球**：
  - 呼吸动画（吸引注意）
  - 点击打开对话窗口

### 对话窗口

- 聊天气泡样式（用户/AI 区分）
- 关键词智能响应
- 情绪检测和关怀
- 自动滚动到底部

---

## 🔑 核心算法

### 经验值曲线

```python
XP_for_level(n) = BASE_XP * (MULTIPLIER ^ (n - 1))

示例（BASE=100, MULTIPLIER=1.5）：
- Level 1→2: 100 XP
- Level 2→3: 150 XP
- Level 3→4: 225 XP
- Level 10: ~3,800 XP
```

### 奖励计算

```python
总 XP = 基础 XP (50) + 长度奖励（每10字 +1，最多100）
属性点 = 每个匹配属性 5-20 点（基于关键词数量）
评语 = 根据主要属性生成激励评语
```

---

## 🤝 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

**优先贡献领域：**
1. UI/UX 改进（动画、可视化、主题）
2. AI 功能增强（模板、关键词、LLM 集成）
3. 数据可视化（成长曲线、统计报表）
4. 成就系统（界面、触发逻辑、动画）
5. 测试（单元测试、UI 测试、性能测试）

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

感谢所有为个人成长努力的你！

---

**启航者，让成长可见。**
