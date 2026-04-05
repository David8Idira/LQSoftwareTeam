# Harness Engineering 与软件实施团队融合分析

> 研究目标：将 claw-code 的 harness engineering AI新范式，融合进软件实施团队工作经历
> 
> 基于 ultraworkers/claw-code 源码分析 | 2026-04-05

---

## 一、Harness Engineering 核心范式

### 1.1 根本理念：人类设定方向，Claws执行劳动

claw-code 展示了一套全新的 AI 驱动软件开发范式：

| 传统模式 | Harness 模式 |
|---------|--------------|
| 人类在终端全程操控 | 人类通过 Discord/Chat 下达方向性指令 |
| 单agent顺序执行 | 多agent并行协调（Architect/Executor/Reviewer） |
| 状态靠日志推断 | 状态机 + 事件驱动（typed events） |
| 失败后人工介入 | 已知失败模式自动恢复（Recovery Recipes） |
| 上下文窗口管理一切 | 事件路由外置（clawhip），保持上下文纯净 |

### 1.2 三层核心系统

```
┌─────────────────────────────────────────────────────────┐
│  Discord Channel（人类指令入口）                          │
├─────────────────────────────────────────────────────────┤
│  OmX (oh-my-codex)     ← 工作流编排层                    │
│  - planning keywords    - 执行模式                        │
│  - 持久验证循环        - 并行多agent工作流               │
├─────────────────────────────────────────────────────────┤
│  OmO (oh-my-openagent) ← 多agent协调层                  │
│  - 规划/handoff        - 分歧解决                       │
│  - 跨agent验证循环                                       │
├─────────────────────────────────────────────────────────┤
│  clawhip              ← 事件与通知路由层                 │
│  - 监听 git/tmux/GitHub events                         │
│  - agent生命周期事件     - 频道分发                      │
│  （保持agent上下文纯净，不被状态更新污染）                  │
├─────────────────────────────────────────────────────────┤
│  Coding Agent（Claude Code / Codex）                    │
│  - 专注实现，不负责通知路由                              │
└─────────────────────────────────────────────────────────┘
```

### 1.3 关键设计原则（Product Principles）

| # | 原则 | 含义 |
|---|------|------|
| 1 | State machine first | 每个worker有明确的生命周期状态 |
| 2 | Events over scraped prose | 通道输出来源于typed events，而非日志解析 |
| 3 | Recovery before escalation | 已知失败模式先自动恢复，再升级 |
| 4 | Branch freshness before blame | 先检测stale branches，再归因测试失败 |
| 5 | Partial success is first-class | MCP部分启动成功也需结构化报告 |
| 6 | Terminal is transport, not truth | tmux/TUI是实现细节，编排状态在其之上 |
| 7 | Policy is executable | merge/retry/rebase/清理/升级规则机器可执行 |

### 1.4 当前痛点与解决路径

| 痛点 | Harness解决 |
|------|-------------|
| Session启动脆弱 | Ready-handshake生命周期（spawning→trust_required→ready_for_prompt） |
| 真相分散在多层 | clawhip统一事件流 |
| 事件太像日志 | Typed events（lane.started/lane.green/lane.red等） |
| 恢复循环太人工 | Recovery recipes编码已知恢复步骤 |
| Branch新鲜度未强制 | stale-branch检测 + 自动rebase |
| 插件/MCP失败分类不清 | Failure taxonomy（9类标准失败分类） |
| 人类UX泄露到claw流程 | 显式agent状态转换和控制API |

---

## 二、软件实施团队现状分析

### 2.1 团队架构

```
软件实施团队 (software-team/)
├── software_team.py      # 主控程序
├── Agent角色:
│   ├── Master           # 主控：任务协调、流程控制
│   ├── Analyst          # 分析：需求、市场、竞品
│   ├── Designer         # 设计：架构、技术选型
│   ├── Coder            # 编码：功能实现
│   ├── Tester           # 测试：单元/集成/性能
│   ├── Packager         # 打包：构建、发布
│   └── Researcher       # 研究：GitHub热门分析
└── 工作流: 需求→分析→设计→实现→测试→打包→发布
```

### 2.2 现有能力评估

| 维度 | 现状 | Harness差距 |
|------|------|-------------|
| **工作流编排** | 软件team.py顺序驱动 | 无并行、无状态机 |
| **事件机制** | 无 | clawhip事件路由缺失 |
| **生命周期** | 隐式 | 无ready/trust/blocked状态 |
| **失败恢复** | 手动 | 无Recovery Recipes |
| **分支管理** | 无 | 无stale-branch检测 |
| **人类接口** | 命令行 | 无Discord/Chat接口 |
| **验证循环** | 无 | 无持续验证机制 |

---

## 三、融合路径：分阶段升级方案

### 3.1 第一阶段：事件驱动架构（Event-Native）

**目标**：将团队从"轮询/日志推断"升级到"事件驱动"

```
当前:
  while True:
    check_logs()      # 被动推断
    infer_state()     # 日志解析
    decide_action()   # 模糊判断

Harness模式:
  events.subscribe('lane.*', handler)  # 主动订阅
  events.on('lane.failed', classify_and_recover)  # typed处理
```

**具体改进**：

1. **引入事件总线**
   ```python
   # 事件类型定义
   class TeamEvent(Enum):
       TASK_STARTED = "task.started"
       TASK_BLOCKED = "task.blocked"  
       TASK_COMPLETED = "task.completed"
       AGENT_READY = "agent.ready"
       BRANCH_STALE = "branch.stale"
       TEST_GREEN = "test.green"
       TEST_RED = "test.red"
       UPLOAD_SUCCESS = "upload.success"
       UPLOAD_FAILED = "upload.failed"
   ```

2. **状态机改造**
   ```python
   # Agent生命周期状态
   class AgentState(Enum):
       IDLE = "idle"
       SPAWNING = "spawning"
       TRUST_REQUIRED = "trust_required"
       READY = "ready_for_prompt"
       RUNNING = "running"
       BLOCKED = "blocked"
       FINISHED = "finished"
       FAILED = "failed"
   ```

### 3.2 第二阶段：Recovery Recipes（自动恢复）

**目标**：编码常见失败的自动恢复步骤

| 失败类型 | 检测方式 | 自动恢复步骤 |
|----------|----------|--------------|
| Git认证失败 | upload failed + auth error | refresh token → retry |
| 分支落后 | branch.stale event | auto rebase main → retry |
| 测试超时 | test timeout | rerun with longer timeout |
| API限流 | 429 response | wait 60s → exponential backoff |
| Trust prompt阻塞 | trust_required state | auto-accept if allowlisted |

```python
RECOVERY_RECIPES = {
    'git_auth_failed': {
        'max_retries': 3,
        'backoff': 30,
        'action': 'refresh_token_and_retry'
    },
    'branch_stale': {
        'action': 'auto_rebase_or_merge_forward'
    },
    'test_timeout': {
        'action': 'rerun_with_extended_timeout',
        'timeout_multiplier': 2
    }
}
```

### 3.3 第三阶段：多agent协调（OmO模式）

**当前问题**：
- Analyst和Designer可能产出冲突
- Coder发现设计不可行时无结构化反馈
- Reviewer意见分散在代码注释中

**Harness解决**：
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Architect  │ ←→  │   Executor  │ ←→  │   Reviewer  │
│  (Designer) │     │   (Coder)   │     │  (Tester)   │
└─────────────┘     └─────────────┘     └─────────────┘
       ↓                   ↓                   ↓
       └───────────────────┼───────────────────┘
                           ↓
                    OmO 协调循环
                    - 分歧解决协议
                    - Handoff确认
                    - 验证通过门控
```

### 3.4 第四阶段：人类接口升级

**目标**：从命令行升级到Chat接口

| 当前 | 目标 |
|------|------|
| 手动运行 python software_team.py | Discord/飞书发消息 |
| 结果输出到终端 | 事件推送到频道 |
| 人工监控进度 | 异常自动告警 |
| 手动检查分支状态 | stale检测自动通知 |

---

## 四、立即可落地的改进

### 4.1 高优先级（1-2天内可完成）

**① 添加Agent生命周期状态**
```python
# 在software_team.py中为每个Agent添加状态机
self.state = AgentState.IDLE

def transition_to(self, new_state):
    self.state = new_state
    event_bus.emit(f'agent.{new_state.value}', {
        'agent': self.role,
        'timestamp': now()
    })
```

**② 失败分类日志**
```python
class FailureType(Enum):
    PROMPT_DELIVERY = "prompt_delivery"
    TRUST_GATE = "trust_gate"
    BRANCH_DIVERGENCE = "branch_divergence"
    COMPILE_ERROR = "compile"
    TEST_FAILURE = "test"
    UPLOAD_FAILED = "upload"
    INFRA = "infra"
```

**③ 添加Git分支新鲜度检测**
```bash
# 在upload前自动检查
git fetch origin
local=$(git rev-parse HEAD)
remote=$(git rev-parse origin/main)
if [ "$local" != "$remote" ]; then
    echo "⚠️ Branch is stale, rebasing..."
    git rebase origin/main
fi
```

### 4.2 中优先级（1周内）

**④ 事件总线实现**
```python
# 采用Redis Pub/Sub或简单Python EventBus
class TeamEventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)
    
    def subscribe(self, event_pattern, handler):
        self.subscribers[event_pattern].append(handler)
    
    def emit(self, event_type, data):
        for pattern, handlers in self.subscribers.items():
            if fnmatch(event_type, pattern):
                for h in handlers: h(event_type, data)
```

**⑤ Recovery Recipes框架**
```python
def with_recovery(operation, failure_handlers):
    for attempt in range(MAX_RETRIES):
        try:
            return operation()
        except Exception as e:
            failure_type = classify(e)
            if failure_type in failure_handlers:
                failure_handlers[failure_type]['action']()
            else:
                raise
```

### 4.3 低优先级（长期）

**⑥ Discord/飞书集成**
- 将事件路由到即时通讯频道
- 人类通过聊天下达方向性指令
- 异常时主动推送告警

**⑦ 凌晨学习模式增强**
- 分析claw-code的"autonomous loop"
- 实现：分析→优化→PR→通知 的完全自主执行

---

## 五、能力矩阵对比

| 能力维度 | 当前软件实施团队 | 目标（Harness化） | 提升幅度 |
|----------|-----------------|------------------|---------|
| 状态透明度 | 1/5 | 5/5 | +80% |
| 失败自愈 | 1/5 | 4/5 | +60% |
| 人类接口 | 2/5 | 5/5 | +60% |
| 并行效率 | 1/5 | 4/5 | +60% |
| 上下文纯净度 | 1/5 | 5/5 | +80% |

---

## 六、参考资源

- **claw-code仓库**: `/root/workspace/claw-code-main/`
- **Rust实现**: `/root/workspace/claw-code-main/rust/`
- **Philosophy**: PHILOSOPHY.md - "Humans set direction; claws perform the labor"
- **Roadmap**: ROADMAP.md - Phase 1-7详细规划
- **OmX工作流**: [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
- **clawhip事件路由**: [clawhip](https://github.com/Yeachan-Heo/clawhip)
- **OmO多agent协调**: [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)

---

*分析基于 ultraworkers/claw-code v6b73f7f | 2026-04-05*
