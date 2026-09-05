# 贡献指南

感谢你对 functional-monism 项目的关注！

## 如何贡献

### 报告问题

- 使用 GitHub Issues 提交 bug 报告
- 请包含最小可复现示例
- 注明你的运行环境（Python 版本、操作系统、依赖版本）

### 提交代码

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 编写代码并添加测试
4. 确保所有测试通过
5. 提交 Pull Request

### 代码规范

- 遵循 PEP 8 编码风格
- 所有公共函数需包含 docstring
- 核心数学模块需包含数学背景说明

### 公理贡献

如需添加新公理或定理：

1. 在 `axioms/` 目录下创建对应的 Markdown 文件
2. 包含形式化陈述、数学表达、直观解释和推论
3. 定理需包含从公理的推导过程

### 模型贡献

1. 新模型放置在 `src/models/` 下
2. 需包含单元测试
3. 提供示例脚本在 `src/examples/` 中