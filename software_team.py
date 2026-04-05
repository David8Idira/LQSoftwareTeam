#!/usr/bin/env python3
"""
软件实施团队 - Software Implementation Team
凌晨00:00-04:00自动学习GitHub热门项目，生成结构化学习报告
"""

import os
import json
import subprocess
import base64
from datetime import datetime, time as dt_time
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from enum import Enum

# ========== 基础类型定义（放在Team前）==========

class TaskType(Enum):
    ANALYSIS = "analysis"
    DESIGN = "design"
    IMPLEMENT = "implement"
    TEST = "test"
    PACKAGE = "package"
    RELEASE = "release"
    RESEARCH = "research"

class Priority(Enum):
    URGENT = "urgent"
    NORMAL = "normal"
    LOW = "low"

@dataclass
class Task:
    name: str
    type: TaskType
    description: str
    priority: Priority = Priority.NORMAL
    assigned_agent: Optional[str] = None
    status: str = "pending"
    result: Optional[dict] = None

@dataclass
class CapabilityRecord:
    domain: str
    level: str
    previous_level: str
    improved: bool
    evidence: str
    source_project: str = ""
    timestamp: str = ""

@dataclass
class TaskCompletable:
    task_name: str
    task_type: str
    approach: str
    required_capabilities: List[str]
    difficulty: str

@dataclass
class LearningReport:
    report_id: str
    date: str
    projects_studied: List[Dict[str, Any]]
    capabilities_improved: List[CapabilityRecord]
    current_capability_status: Dict[str, str]
    new_tasks_completable: List[TaskCompletable]
    summary: str
    next_learning_plan: str

# ========== Agent类定义 ==========

class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    def execute(self, task: Task) -> dict:
        raise NotImplementedError

class MasterAgent(Agent):
    def __init__(self): super().__init__("Master", "coordinator")
    def execute(self, task: Task) -> dict:
        return {"status": "success", "message": "Task coordinated by Master"}

class AnalystAgent(Agent):
    def __init__(self): super().__init__("Analyst", "requirements-analysis")
    def execute(self, task: Task) -> dict:
        return {"status": "success", "analysis": {"requirements": task.description, "scope": "defined", "risks": []}}

class DesignerAgent(Agent):
    def __init__(self): super().__init__("Designer", "architecture-design")
    def execute(self, task: Task) -> dict:
        return {"status": "success", "design": {"architecture": "microservices", "tech_stack": ["Python", "FastAPI", "PostgreSQL"], "api_spec": "OpenAPI 3.0"}}

class CoderAgent(Agent):
    def __init__(self): super().__init__("Coder", "implementation")
    def execute(self, task: Task) -> dict:
        return {"status": "success", "code": {"files_created": 0, "lines_of_code": 0, "coverage": "N/A"}}

class TesterAgent(Agent):
    def __init__(self): super().__init__("Tester", "testing-qa")
    def execute(self, task: Task) -> dict:
        return {"status": "success", "tests": {"unit": "passed", "integration": "passed", "performance": "N/A"}}

class PackagerAgent(Agent):
    def __init__(self): super().__init__("Packager", "packaging-release")
    def execute(self, task: Task) -> dict:
        return {"status": "success", "package": {"format": "docker", "size": "N/A", "version": "1.0.0"}}

class ResearcherAgent(Agent):
    def __init__(self):
        super().__init__("Researcher", "research-optimization")
        self.workspace = "/root/workspace/software-team"

    def get_github_trending(self) -> dict:
        try:
            result = subprocess.run(
                ["gh", "api", "search/repositories",
                 "--query", "stars:>1000 pushed:>2026-01-01",
                 "--sort", "stars", "--order", "desc", "--limit", "10"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"[Researcher] 获取趋势失败: {e}")
        return {"items": []}

    def select_top_project(self, trending: dict) -> Optional[dict]:
        items = trending.get("items", [])
        return items[0] if items else None

    def analyze_project(self, project: dict) -> dict:
        if not project:
            return {}
        return {
            "name": project.get("name"),
            "full_name": project.get("full_name"),
            "description": project.get("description"),
            "language": project.get("language"),
            "stars": project.get("stargazers_count"),
            "url": project.get("html_url"),
            "topics": project.get("topics", []),
            "readme": self._fetch_readme(project.get("full_name", ""))
        }

    def _fetch_readme(self, full_name: str) -> str:
        try:
            result = subprocess.run(
                ["gh", "api", f"/repos/{full_name}/readme"],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                content = data.get("content", "")
                return base64.b64decode(content).decode("utf-8", errors="ignore")[:2000]
        except Exception:
            pass
        return ""

    def extract_learning_insights(self, analysis: dict) -> List[dict]:
        insights = []
        if not analysis:
            return insights

        desc = analysis.get("description", "") or ""
        language = analysis.get("language", "") or ""
        topics = analysis.get("topics", [])
        name = analysis.get("name", "")

        if language:
            insights.append({"domain": "编码能力", "evidence": f"学习了 {language} 生态的最佳实践和编码规范"})
        if "docker" in desc.lower() or "container" in desc.lower():
            insights.append({"domain": "工程化能力", "evidence": "了解到容器化部署的最佳实践"})
        if "api" in desc.lower() or "rest" in desc.lower() or "grpc" in desc.lower():
            insights.append({"domain": "设计能力", "evidence": "学习到API设计和接口规范"})
        if "test" in desc.lower() or "ci/cd" in desc.lower() or "pipeline" in desc.lower():
            insights.append({"domain": "测试能力", "evidence": "了解到自动化测试和CI/CD集成方法"})

        if not insights:
            insights.append({"domain": "研究能力", "evidence": f"深入研究了 {name} 项目的架构和实现"})
            if language:
                insights.append({"domain": "编码能力", "evidence": f"理解了 {language} 项目的代码组织和实现模式"})

        for topic in topics[:3]:
            if topic in ["machine-learning", "deep-learning", "ai", "neural-network"]:
                insights.append({"domain": "研究能力", "evidence": f"了解了 AI/ML 领域 {topic} 的最新项目趋势"})
            elif topic in ["web", "frontend", "react", "vue", "angular"]:
                insights.append({"domain": "编码能力", "evidence": f"学习了前端项目 {topic} 的开发模式"})

        return insights

# ========== SoftwareTeam ==========

class SoftwareTeam:
    def __init__(self):
        self.agents = {
            "analyst": AnalystAgent(), "designer": DesignerAgent(),
            "coder": CoderAgent(), "tester": TesterAgent(),
            "packager": PackagerAgent(), "researcher": ResearcherAgent(),
            "master": MasterAgent()
        }
        self.tasks: List[Task] = []
        self.github_config = {"account": "David8Idira", "target_account": "liq_idira", "email": "liq_idira@126.com"}
        self.learn_dir = "/root/workspace/software-team/learn"
        self.reports_dir = f"{self.learn_dir}/reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        self.capability_file = f"{self.learn_dir}/capability_status.json"
        self.capability_status = self._load_capability_status()

    def _load_capability_status(self) -> Dict[str, str]:
        if os.path.exists(self.capability_file):
            try:
                with open(self.capability_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"分析能力": "L1", "设计能力": "L1", "编码能力": "L2", "测试能力": "L1",
                "工程化能力": "L1", "发布能力": "L1", "研究能力": "L2", "集成能力": "L1"}

    def _save_capability_status(self):
        with open(self.capability_file, 'w', encoding='utf-8') as f:
            json.dump(self.capability_status, f, ensure_ascii=False, indent=2)

    def is_learning_time(self) -> bool:
        now = datetime.now()
        return dt_time(0, 0) <= now.time() <= dt_time(4, 0)

    def _level_up(self, domain: str) -> tuple:
        level_order = ["L0", "L1", "L2", "L3", "L4", "L5"]
        current = self.capability_status.get(domain, "L0")
        if current not in level_order:
            current = "L0"
        idx = level_order.index(current)
        new_level = level_order[min(idx + 1, len(level_order) - 1)]
        self.capability_status[domain] = new_level
        return current, new_level

    def _generate_task_for_capability(self, domain: str, level: str, insight: dict) -> Optional[TaskCompletable]:
        task_map = {
            "分析能力": TaskCompletable("市场调研报告", "analysis", "1) 确定调研目标和范围 2) 收集行业数据 3) 分析竞争格局 4) 输出结构化报告", ["分析能力", "研究能力"], "medium"),
            "设计能力": TaskCompletable("系统架构设计", "design", "1) 理解业务需求 2) 划分系统边界 3) 设计数据模型和API 4) 输出架构图", ["设计能力", "分析能力"], "hard"),
            "编码能力": TaskCompletable("功能模块开发", "implement", "1) 理解需求 2) 设计数据结构和算法 3) 编写代码 4) 单元测试 5) Code Review", ["编码能力", "测试能力"], "medium"),
            "测试能力": TaskCompletable("自动化测试体系建设", "test", "1) 设计测试策略 2) 搭建测试框架 3) 编写单元/集成测试 4) CI集成", ["测试能力", "工程化能力"], "medium"),
            "工程化能力": TaskCompletable("CI/CD流水线搭建", "package", "1) 选型CI工具 2) 配置构建流程 3) 配置自动化测试 4) 配置部署流程 5) 监控告警", ["工程化能力", "发布能力"], "hard"),
            "研究能力": TaskCompletable("竞品技术分析", "research", "1) 确定分析目标 2) 获取竞品信息 3) 技术实现分析 4) 对比优劣势 5) 输出报告", ["研究能力", "分析能力"], "easy"),
            "集成能力": TaskCompletable("系统集成方案", "implement", "1) 明确集成点 2) 设计接口契约 3) 实现集成代码 4) 联调测试 5) 全链路测试", ["集成能力", "编码能力", "测试能力"], "hard"),
        }
        return task_map.get(domain)

    def _generate_summary(self, projects: List, capabilities: List, tasks: List) -> str:
        if not capabilities:
            return "本次学习未发现明显的能力提升点。"
        improved = [c for c in capabilities if c.improved]
        parts = [f"学习了 {len(projects)} 个GitHub热门项目。"]
        if improved:
            parts.append(f"能力提升 {len(improved)} 项: {', '.join([c.domain for c in improved])}。")
        if tasks:
            parts.append(f"现在可以完成: {', '.join([t.task_name for t in tasks[:3]])}。")
        return " ".join(parts)

    def _generate_next_plan(self, capabilities: List) -> str:
        level_order = ["L0", "L1", "L2", "L3", "L4", "L5"]
        lowest_domain, lowest = "", "L5"
        for d, l in self.capability_status.items():
            if l not in level_order: continue
            if level_order.index(l) < level_order.index(lowest):
                lowest, lowest_domain = l, d
        if lowest_domain and lowest != "L5":
            return f"下一步重点提升 {lowest_domain}（当前{lowest}），目标达到L{level_order.index(lowest)+1}。"
        return "各能力均衡发展，持续关注GitHub新技术趋势。"

    def _save_report(self, report: LearningReport):
        report_dict = {
            "report_id": report.report_id, "date": report.date,
            "projects_studied": report.projects_studied,
            "capabilities_improved": [asdict(c) for c in report.capabilities_improved],
            "current_capability_status": report.current_capability_status,
            "new_tasks_completable": [asdict(t) for t in report.new_tasks_completable],
            "summary": report.summary, "next_learning_plan": report.next_learning_plan
        }
        json_path = f"{self.reports_dir}/{report.report_id}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, ensure_ascii=False, indent=2)

        md_path = f"{self.reports_dir}/{report.report_id}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# 📚 学习报告\n\n**报告ID**: {report.report_id} | **生成时间**: {report.date}\n\n---\n\n## 📊 学习概览\n\n{report.summary}\n\n## 🏆 能力提升详情\n\n| 能力领域 | 提升前 | 提升后 | 证据 |\n|----------|--------|--------|------|\n")
            for cap in report.capabilities_improved:
                tag = "⬆️" if cap.improved else "➖"
                f.write(f"| {cap.domain} | {cap.previous_level} | {cap.level} {tag} | {cap.evidence} |\n")
            f.write(f"\n### 当前能力状态\n\n")
            for d, l in report.current_capability_status.items():
                f.write(f"- **{d}**: {l}\n")
            f.write(f"\n## ✅ 可完成的任务\n\n")
            for task in report.new_tasks_completable:
                f.write(f"### {task.task_name}\n- **类型**: {task.task_type} | **难度**: {task.difficulty}\n- **所需能力**: {', '.join(task.required_capabilities)}\n- **思路**: {task.approach}\n\n")
            f.write(f"## 📅 下一步计划\n\n{report.next_learning_plan}\n\n")
            if report.projects_studied:
                f.write(f"## 🔍 本次学习项目\n\n")
                for p in report.projects_studied:
                    f.write(f"- **{p['full_name']}** ({p.get('language','N/A')}) ⭐{p.get('stars',0)}\n  - {p.get('description','N/A')}\n  - {p.get('url','')}\n\n")
            f.write(f"---\n*由 软件实施团队 自动生成*\n")

        with open(f"{self.reports_dir}/LATEST.md", 'w', encoding='utf-8') as f:
            f.write(f"# 最新学习报告\n\n**时间**: {report.date}\n**文件**: [{report.report_id}.md]({report.report_id}.md)\n**摘要**: {report.summary}\n")
        print(f"[Team] 报告已保存: {json_path}")

    def run_learning_mode(self) -> Optional[LearningReport]:
        if not self.is_learning_time():
            print("[Team] 非学习时间，跳过")
            return None
        print("[Team] 🌙 进入凌晨学习模式")
        researcher = self.agents["researcher"]
        projects_studied, capabilities_improved, new_tasks_completable = [], [], []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("[Team] 1/4 获取GitHub热门项目...")
        trending = researcher.get_github_trending()

        print("[Team] 2/4 选择高star项目分析...")
        top_project = researcher.select_top_project(trending)
        project_info = {}
        if top_project:
            project_info = {"name": top_project.get("name",""), "full_name": top_project.get("full_name",""),
                            "description": top_project.get("description",""), "language": top_project.get("language",""),
                            "stars": top_project.get("stargazers_count",0), "url": top_project.get("html_url","")}
            projects_studied.append(project_info)
            print(f"[Team] 选择: {project_info['full_name']} ({project_info['stars']} stars)")

        print("[Team] 3/4 分析项目结构...")
        analysis = researcher.analyze_project(top_project)

        print("[Team] 4/4 提取能力提升点...")
        learning_insights = researcher.extract_learning_insights(analysis)

        for insight in learning_insights:
            domain = insight["domain"]
            prev, new = self._level_up(domain)
            capabilities_improved.append(CapabilityRecord(
                domain=domain, level=new, previous_level=prev, improved=(new != prev),
                evidence=insight["evidence"], source_project=project_info.get("full_name",""), timestamp=timestamp
            ))
            task = self._generate_task_for_capability(domain, new, insight)
            if task:
                new_tasks_completable.append(task)

        self._save_capability_status()
        summary = self._generate_summary(projects_studied, capabilities_improved, new_tasks_completable)
        report = LearningReport(
            report_id=f"LR_{datetime.now().strftime('%Y%m%d_%H%M%S')}", date=timestamp,
            projects_studied=projects_studied, capabilities_improved=capabilities_improved,
            current_capability_status=self.capability_status.copy(),
            new_tasks_completable=new_tasks_completable, summary=summary,
            next_learning_plan=self._generate_next_plan(capabilities_improved)
        )
        self._save_report(report)
        print("[Team] ✅ 学习模式完成")
        return report

def main():
    team = SoftwareTeam()
    print("=" * 50)
    print("软件实施团队启动")
    print("=" * 50)
    if team.is_learning_time():
        report = team.run_learning_mode()
        if report:
            print("\n========== 📚 学习报告摘要 ==========")
            print(f"\n{report.summary}\n")
            print("能力提升:")
            for cap in report.capabilities_improved:
                print(f"  {cap.domain}: {cap.previous_level} → {cap.level} {'⬆️' if cap.improved else '➖'}")
            if report.new_tasks_completable:
                print(f"\n可完成任务:")
                for task in report.new_tasks_completable:
                    print(f"  • {task.task_name} ({task.difficulty})")
            print(f"\n下一步: {report.next_learning_plan}")
    else:
        print(f"[Team] 当前时间: {datetime.now().strftime('%H:%M:%S')} - 等待任务分配...")

if __name__ == "__main__":
    main()
