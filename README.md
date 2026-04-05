# 软件实施团队 - Software Implementation Team

基于 OpenClaw + OpenCode + OpenSwarm 的多智能体协作系统

## 📋 头脑风暴

### LRuoYi-OA项目 → AI-OA项目

软件实施团队已完成LRuoYi-OA项目的头脑风暴：

| 角色 | 职责 | 观点 |
|------|------|------|
| Master | 项目经理汇总 | Sprint划分(4个)、交付清单、风险缓解 |
| Analyst | 市场分析 | 优先F2/F4快速验证价值 |
| Designer | 架构设计 | 微服务按领域划分，统一AI网关 |
| Coder | 开发实现 | P0优先级F1/F2/F4 |
| Tester | 测试策略 | AI测试+自动化流水线 |

头脑风暴报告：`docs/AI-OA_头脑风暴报告.md`

## 🎯 团队组成

| Agent | 角色 | 职责 |
|-------|------|------|
| Master | 主控 | 任务协调、流程控制 |
| Analyst | 分析 | 需求分析、市场调研、竞品分析 |
| Designer | 设计 | 架构设计、技术选型、接口设计 |
| Coder | 编码 | 代码开发、功能实现、集成 |
| Tester | 测试 | 单元测试、集成测试、性能测试 |
| Packager | 打包 | 构建、打包、版本管理、发布 |
| Researcher | 研究 | GitHub热门项目分析、优化 |

## 📋 工作流程

```
需求 → 分析 → 设计 → 实现 → 测试 → 打包 → 发布
  ↓
凌晨学习模式: 00:30 - 06:00
  ↓
分析GitHub热门项目 → 优化 → 上传到David8Idira账号 (LQ前缀)
```

## 🚀 快速开始

### 1. 团队启动

```bash
cd /root/workspace/software-team
python3 software_team.py
```

### 2. 凌晨学习模式 (自动)

```bash
# 设置Cron任务 (已配置)
crontab -e
# 添加: 30 0 * * * /root/workspace/software-team/configs/team-cron.sh

# 或手动运行
/root/workspace/software-team/configs/team-cron.sh
```

## 🌙 凌晨学习模式

每天 00:30 - 06:00 无任务时自动执行:

1. **获取GitHub热门项目** - star增长最快的开源项目
2. **分析项目结构** - 技术栈、架构设计、代码质量
3. **优化项目** - 性能优化、代码重构、功能增强
4. **致谢上传** - 添加LQ前缀，上传到李迁GitHub账号

### 上传格式

```
项目名: LQ{original_name}
描述: LQ优化版 - {original_description}
```

### 致谢内容

README.md自动添加:

```markdown
---
# 致谢

本项目基于 [OriginalName](url) 优化而来。

## 原项目信息
- **原作者**: xxx
- **原始描述**: xxx
- **Star数**: xxx
- **优化日期**: 2026-04-03

## 优化内容
- 性能优化
- 代码重构
- 文档完善
```

## 📁 目录结构

```
software-team/
├── software_team.py          # 主程序
├── upload_to_liqian.py       # 上传到李迁GitHub
├── agents/                   # Agent定义
├── configs/
│   ├── swarm.config.json     # OpenSwarm配置
│   └── team-cron.sh         # Cron任务脚本
├── workflows/                # 工作流程定义
├── learn/                   # 学习成果
│   └── trending/            # 热门项目缓存
└── logs/                    # 日志文件
```

## ⚙️ 配置

### GitHub账号

当前配置:
- **操作账号**: David8Idira
- **目标账号**: liq_idira (李迁)
- **邮箱**: liq_idira@126.com

### 上传到李迁账号

需要配置Token:
```bash
export GITHUB_LIQ_TOKEN="your-token-here"
python3 upload_to_liqian.py --project /path/to/project --name "OriginalName"
```

## 🔧 工具集成

| 工具 | 版本 | 用途 |
|------|------|------|
| OpenClaw | 2026.3.28 | 主智能体框架 |
| OpenCode | 1.3.13 | CLI编码工具 |
| OpenSwarm | 0.1.1 | 多智能体编排 |
| Claude Code CLI | 2.1.89 | 辅助编码 |
| RobinPath CLI | 4.5.0 | 脚本自动化 |

## 📊 任务类型

| 类型 | 优先级 | Agent |
|------|--------|-------|
| analysis | normal | Analyst |
| design | normal | Designer |
| implement | normal | Coder |
| test | normal | Tester |
| package | normal | Packager |
| release | urgent | Packager |
| research | low | Researcher |

## 📝 日志

日志位置: `/root/workspace/software-team/logs/`

---

*Last updated: 2026-04-03*
