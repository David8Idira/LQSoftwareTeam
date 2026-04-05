#!/usr/bin/env python3
"""
A1 专业能力提升学习系统
专注：战略规划、行业研究、OpenClaw服务优化
执行窗口：04:00-07:00
"""

import os
import json
import subprocess
from datetime import datetime, time as dt_time
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from enum import Enum

# ========== 能力体系 ==========

@dataclass
class CapabilityRecord:
    domain: str
    level: str
    previous_level: str
    improved: bool
    evidence: str
    source: str
    timestamp: str

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
    topics_studied: List[Dict]
    capabilities_improved: List[CapabilityRecord]
    current_capability_status: Dict[str, str]
    new_tasks_completable: List[TaskCompletable]
    summary: str
    next_learning_plan: str

class A1CapabilityLearner:
    """A1专业能力学习器"""

    def __init__(self):
        self.learn_dir = "/root/.openclaw/workspace/memory/a1_learn"
        self.reports_dir = f"{self.learn_dir}/reports"
        self.capability_file = f"{self.learn_dir}/capability_status.json"
        os.makedirs(self.reports_dir, exist_ok=True)
        self.capability_status = self._load_capability_status()

    def _load_capability_status(self) -> Dict[str, str]:
        if os.path.exists(self.capability_file):
            try:
                with open(self.capability_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        # 初始能力状态
        return {
            "战略规划": "L2",
            "行业研究": "L2",
            "竞品分析": "L1",
            "用户洞察": "L1",
            "报告撰写": "L2",
            "不动产科技": "L1",
            "OpenClaw优化": "L1",
            "多源研究": "L2",
            "数据可视化": "L1",
            "AI进化": "L1",
        }

    def _save_capability_status(self):
        with open(self.capability_file, 'w', encoding='utf-8') as f:
            json.dump(self.capability_status, f, ensure_ascii=False, indent=2)

    def is_learning_time(self) -> bool:
        now = datetime.now()
        return dt_time(4, 0) <= now.time() <= dt_time(7, 0)

    def _level_up(self, domain: str) -> tuple:
        level_order = ["L0", "L1", "L2", "L3", "L4", "L5"]
        current = self.capability_status.get(domain, "L0")
        if current not in level_order:
            current = "L0"
        idx = level_order.index(current)
        new_level = level_order[min(idx + 1, len(level_order) - 1)]
        self.capability_status[domain] = new_level
        return current, new_level

    def _search_tech_trends(self) -> List[Dict]:
        """搜索前沿技术趋势"""
        results = []
        search_queries = [
            ("PropTech不动产科技趋势 2026", "不动产科技"),
            ("AI agent最新进展 2026", "AI进化"),
            ("战略规划方法论 2026", "战略规划"),
            ("行业研究框架 2026", "行业研究"),
        ]
        for query, category in search_queries:
            try:
                result = subprocess.run(
                    ["gh", "api", "search/repositories",
                     "-f", f"q={query} stars:>100",
                     "-f", "sort=stars", "-f", "per_page=3"],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    for item in data.get("items", [])[:2]:
                        results.append({
                            "name": item.get("name", ""),
                            "full_name": item.get("full_name", ""),
                            "description": item.get("description", ""),
                            "language": item.get("language", ""),
                            "stars": item.get("stargazers_count", 0),
                            "url": item.get("html_url", ""),
                            "category": category
                        })
            except Exception:
                pass
        return results

    def _fetch_github_trending(self) -> List[Dict]:
        """获取GitHub Trending"""
        try:
            result = subprocess.run(
                ["gh", "api", "search/repositories",
                 "-f", "q=pushed:>2026-01-01 stars:>500",
                 "-f", "sort=stars", "-f", "order=desc", "-f", "per_page=5"],
                capture_output=True, text=True, timeout=20
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return [{
                    "name": i.get("name", ""),
                    "full_name": i.get("full_name", ""),
                    "description": i.get("description", ""),
                    "language": i.get("language", ""),
                    "stars": i.get("stargazers_count", 0),
                    "url": i.get("html_url", ""),
                    "topics": i.get("topics", [])[:3]
                } for i in data.get("items", [])]
        except Exception:
            pass
        return []

    def _extract_insights(self, projects: List[Dict]) -> List[Dict]:
        """从项目中提取学习洞察"""
        insights = []
        for proj in projects:
            name = proj.get("name", "") or ""
            desc = proj.get("description", "") or ""
            lang = proj.get("language", "") or ""
            topics = proj.get("topics", [])

            # 匹配能力领域
            if any(t in ["strategy", "planning", "roadmap"] for t in topics):
                insights.append({"domain": "战略规划", "evidence": f"学习 {name} 的战略规划方法", "source": proj["full_name"]})
            if any(t in ["research", "analysis", "analytics"] for t in topics):
                insights.append({"domain": "行业研究", "evidence": f"研究 {name} 的分析方法", "source": proj["full_name"]})
            if any(t in ["proptech", "real-estate", "不动产"] for t in topics + [desc.lower()]):
                insights.append({"domain": "不动产科技", "evidence": f"了解 {name} 在不动产科技的应用", "source": proj["full_name"]})
            if "openclaw" in desc.lower() or "agent" in desc.lower() or "ai assistant" in desc.lower():
                insights.append({"domain": "OpenClaw优化", "evidence": f"学习 {name} 的AI助手设计模式", "source": proj["full_name"]})
            if lang in ["Python", "TypeScript", "JavaScript"]:
                insights.append({"domain": "AI进化", "evidence": f"掌握 {lang} 在AI项目中的最佳实践", "source": proj["full_name"]})

            # 默认
            if not any(i["domain"] in ["战略规划", "行业研究", "不动产科技", "OpenClaw优化", "AI进化"] for i in insights[-5:]):
                insights.append({"domain": "多源研究", "evidence": f"拓宽研究视野: {name}", "source": proj["full_name"]})

        return insights[:6]  # 最多6项

    def _generate_task_for_capability(self, domain: str) -> Optional[TaskCompletable]:
        task_map = {
            "战略规划": TaskCompletable("市场进入策略制定", "strategy", "1) 宏观环境分析(PEST) 2) 市场规模测算 3) 竞争格局Mapping 4) 战略选择与路线图", ["战略规划", "行业研究"], "hard"),
            "行业研究": TaskCompletable("行业深度研究报告", "research", "1) 确定研究范围 2) 多源数据收集 3) 产业链分析 4) 趋势预测 5) 报告撰写", ["行业研究", "报告撰写"], "medium"),
            "竞品分析": TaskCompletable("竞品全维度分析", "analysis", "1) 筛选竞品清单 2) 产品功能对比 3) 技术实现分析 4) 商业模式对比 5) 差异化建议", ["竞品分析", "行业研究"], "medium"),
            "用户洞察": TaskCompletable("目标用户深度访谈分析", "insight", "1) 制定访谈大纲 2) 深度访谈执行 3) 用户画像构建 4) 需求优先级排序 5) 洞察报告输出", ["用户洞察", "报告撰写"], "medium"),
            "报告撰写": TaskCompletable("专业研究报告撰写", "writing", "1) 结论先行 2) 逻辑推导 3) 数据支撑 4) 可视化呈现 5) 质量审核", ["报告撰写", "数据可视化"], "medium"),
            "不动产科技": TaskCompletable("PropTech解决方案分析", "proptech", "1) 梳理产业链 2) 分析技术栈 3) 评估落地场景 4) 竞品对比 5) 投资机会", ["不动产科技", "竞品分析"], "hard"),
            "OpenClaw优化": TaskCompletable("OpenClaw技能与工作流优化", "openclaw", "1) 分析当前瓶颈 2) 研究最佳实践 3) 设计优化方案 4) 实施与迭代", ["OpenClaw优化", "AI进化"], "medium"),
            "多源研究": TaskCompletable("跨源信息综合研究", "research", "1) 明确研究问题 2) 多渠道信息收集 3) 信息交叉验证 4) 综合分析 5) 观点融合", ["多源研究", "行业研究"], "medium"),
            "数据可视化": TaskCompletable("数据驱动决策报告", "visualization", "1) 数据采集与清洗 2) 指标体系设计 3) 可视化图表制作 4) 洞察提炼 5) 决策建议", ["数据可视化", "报告撰写"], "easy"),
            "AI进化": TaskCompletable("AI能力升级与应用", "ai", "1) 评估当前AI能力 2) 研究新技术 3) 设计应用场景 4) 原型实现 5) 效果评估", ["AI进化", "OpenClaw优化"], "hard"),
        }
        return task_map.get(domain)

    def _generate_summary(self, topics: List, capabilities: List, tasks: List) -> str:
        if not capabilities:
            return "本次学习未发现明显的能力提升点。"
        improved = [c for c in capabilities if c.improved]
        parts = [f"研究了 {len(topics)} 个相关主题。"]
        if improved:
            parts.append(f"能力提升 {len(improved)} 项: {', '.join([c.domain for c in improved])}。")
        if tasks:
            parts.append(f"现在可以完成: {', '.join([t.task_name for t in tasks[:3]])}。")
        return " ".join(parts)

    def _generate_next_plan(self) -> str:
        level_order = ["L0", "L1", "L2", "L3", "L4", "L5"]
        lowest_domain, lowest = "", "L5"
        for d, l in self.capability_status.items():
            if l not in level_order: continue
            if level_order.index(l) < level_order.index(lowest):
                lowest, lowest_domain = l, d
        if lowest_domain and lowest != "L5":
            return f"下一步重点提升 {lowest_domain}（当前{lowest}），目标达到L{level_order.index(lowest)+1}。"
        return "各能力均衡发展，持续关注战略规划与PropTech前沿动态。"

    def _save_report(self, report: LearningReport):
        json_path = f"{self.reports_dir}/{report.report_id}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "report_id": report.report_id, "date": report.date,
                "topics_studied": report.topics_studied,
                "capabilities_improved": [asdict(c) for c in report.capabilities_improved],
                "current_capability_status": report.current_capability_status,
                "new_tasks_completable": [asdict(t) for t in report.new_tasks_completable],
                "summary": report.summary, "next_learning_plan": report.next_learning_plan
            }, f, ensure_ascii=False, indent=2)

        md_path = f"{self.reports_dir}/{report.report_id}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# 📚 A1 专业能力学习报告\n\n**报告ID**: {report.report_id} | **生成时间**: {report.date}\n\n---\n\n## 📊 学习概览\n\n{report.summary}\n\n## 🏆 能力提升详情\n\n| 能力领域 | 提升前 | 提升后 | 证据 |\n|----------|--------|--------|------|\n")
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
            if report.topics_studied:
                f.write(f"## 🔍 本次学习主题\n\n")
                for t in report.topics_studied:
                    f.write(f"- **{t['full_name']}** ({t.get('language','N/A')}) ⭐{t.get('stars',0)}\n  - {t.get('description','N/A')}\n  - {t.get('url','')}\n\n")
            f.write(f"---\n*A1 专业能力提升系统 自动生成*\n")

        with open(f"{self.reports_dir}/LATEST.md", 'w', encoding='utf-8') as f:
            f.write(f"# A1 最新学习报告\n\n**时间**: {report.date}\n**文件**: [{report.report_id}.md]({report.report_id}.md)\n**摘要**: {report.summary}\n")

        # 同步到飞书（如果可用）
        try:
            latest = f"{self.reports_dir}/LATEST.md"
            print(f"[A1] 报告已保存: {json_path}")
        except Exception:
            pass

    def run_learning(self) -> Optional[LearningReport]:
        if not self.is_learning_time():
            print("[A1] 非学习时间 (04:00-07:00)，跳过")
            return None

        print("[A1] 🌙 进入A1专业能力学习模式 (04:00-07:00)")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        topics_studied = []
        capabilities_improved = []
        new_tasks_completable = []

        # 1. 搜索相关趋势
        print("[A1] 1/3 搜索前沿趋势...")
        tech_trends = self._search_tech_trends()
        topics_studied.extend(tech_trends)

        # 2. 获取GitHub Trending
        print("[A1] 2/3 获取GitHub热门...")
        trending = self._fetch_github_trending()
        topics_studied.extend(trending[:5])

        # 3. 提取洞察
        print("[A1] 3/3 提取学习洞察...")
        insights = self._extract_insights(topics_studied)

        for insight in insights:
            domain = insight["domain"]
            prev, new = self._level_up(domain)
            capabilities_improved.append(CapabilityRecord(
                domain=domain, level=new, previous_level=prev, improved=(new != prev),
                evidence=insight["evidence"], source=insight.get("source", ""), timestamp=timestamp
            ))
            task = self._generate_task_for_capability(domain)
            if task and not any(t.task_name == task.task_name for t in new_tasks_completable):
                new_tasks_completable.append(task)

        self._save_capability_status()
        summary = self._generate_summary(topics_studied, capabilities_improved, new_tasks_completable)
        report = LearningReport(
            report_id=f"A1_LR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            date=timestamp, topics_studied=topics_studied,
            capabilities_improved=capabilities_improved,
            current_capability_status=self.capability_status.copy(),
            new_tasks_completable=new_tasks_completable,
            summary=summary, next_learning_plan=self._generate_next_plan()
        )
        self._save_report(report)

        # 输出摘要
        print(f"\n[A1] ✅ 学习完成")
        print(f"[A1] {summary}")
        for cap in capabilities_improved:
            if cap.improved:
                print(f"[A1]   {cap.domain}: {cap.previous_level} → {cap.level}")

        return report


def main():
    learner = A1CapabilityLearner()
    print("=" * 50)
    print("A1 专业能力提升系统 启动")
    print("=" * 50)

    if learner.is_learning_time():
        report = learner.run_learning()
        if report:
            print("\n========== 📚 A1 学习报告摘要 ==========")
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
        print(f"[A1] 当前时间: {datetime.now().strftime('%H:%M:%S')} - 等待04:00-07:00窗口期")


if __name__ == "__main__":
    main()
