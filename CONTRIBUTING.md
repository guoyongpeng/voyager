# 贡献指南

感谢你对启航者 (Voyager) 项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

如果你发现了 bug，请：

1. 检查 [Issues](https://github.com/guoyongpeng/voyager/issues) 中是否已有相关报告
2. 如果没有，创建新 Issue，包含：
   - 详细的问题描述
   - 复现步骤
   - 预期行为 vs 实际行为
   - 系统环境（操作系统、Python 版本等）
   - 错误日志（如果有）

### 提出功能建议

我们欢迎新功能建议！请：

1. 在 Issues 中描述你的想法
2. 说明为什么这个功能有用
3. 提供可能的实现思路（可选）

### 提交代码

#### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/guoyongpeng/voyager.git
cd voyager

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 创建测试数据
python tests/create_test_data.py

# 运行测试
python tests/test_full_workflow.py
```

#### 代码规范

- 遵循 PEP 8 代码风格
- 为新功能添加注释
- 为公共 API 编写文档字符串
- 保持代码简洁清晰

#### Pull Request 流程

1. **Fork 仓库**
   - 点击右上角的 "Fork" 按钮

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **编写代码**
   - 实现你的功能或修复
   - 添加必要的测试
   - 确保代码符合规范

4. **测试**
   ```bash
   # 运行测试
   python tests/test_full_workflow.py

   # 测试 UI
   python main.py
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 简短描述你的更改"
   ```

   提交信息格式：
   - `feat: 新功能`
   - `fix: Bug 修复`
   - `docs: 文档更新`
   - `style: 代码格式调整`
   - `refactor: 重构`
   - `test: 测试相关`
   - `chore: 构建/工具相关`

6. **推送到你的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**
   - 在 GitHub 上打开你的 Fork
   - 点击 "New Pull Request"
   - 填写 PR 描述：
     - 改动的内容
     - 为什么需要这个改动
     - 如何测试

## 开发建议

### 项目结构

```
src/
├── database/     # 数据库管理
├── core/         # 核心业务逻辑（Player, Quest）
├── ai/           # AI 引擎（本地规则 + 可选 LLM）
├── ui/           # UI 组件
│   ├── widgets/  # 自定义组件
│   └── dialogs/  # 对话框
└── utils/        # 工具类
```

### 优先级领域

我们特别欢迎以下方面的贡献：

1. **UI/UX 改进**
   - 动画效果优化
   - 新的可视化组件
   - 主题支持

2. **AI 功能增强**
   - 更多任务拆解模板
   - 改进的情绪检测
   - LLM 集成（智谱 AI）

3. **数据可视化**
   - 成长曲线图
   - 统计报表
   - 导入/导出功能

4. **成就系统**
   - 成就界面
   - 触发逻辑
   - 解锁动画

5. **测试**
   - 单元测试
   - UI 测试
   - 性能测试

### 代码审查

所有 Pull Request 都会经过代码审查。审查重点：

- 代码质量和可读性
- 是否符合项目架构
- 测试覆盖
- 文档完整性
- 向后兼容性

## 行为准则

- 尊重所有贡献者
- 保持友好和建设性的讨论
- 接受建设性的批评
- 专注于对项目最有利的事情

## 联系方式

如有问题，可以：

- 在 Issues 中提问
- 发起 Discussions
- 通过 Pull Request 讨论

## 许可证

通过贡献代码，你同意你的贡献将在 MIT 许可证下发布。

---

再次感谢你的贡献！🎉
