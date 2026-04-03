#!/usr/bin/env python3
"""
上传优化项目到李迁的GitHub账号
需要配置 GitHub Token

使用方式:
    python3 upload_to_liqian.py --project /path/to/project --name "OriginalName"
"""

import argparse
import subprocess
import os
import json
from datetime import datetime

# 李迁的GitHub配置
LIQIAN_CONFIG = {
    "username": "liq_idira",
    "email": "liq_idira@126.com",
    # 需要配置Token才能操作
    "token_env": "GITHUB_LIQ_TOKEN"
}

def get_token():
    """获取GitHub Token"""
    return os.environ.get(LIQIAN_CONFIG["token_env"])

def create_repo(project_name: str, description: str, private: bool = False) -> dict:
    """创建GitHub仓库"""
    token = get_token()
    if not token:
        return {"status": "error", "message": "缺少GitHub Token，请设置 GITHUB_LIQ_TOKEN 环境变量"}
    
    cmd = [
        "gh", "api", "repos",
        "-f", f"name={project_name}",
        "-f", f"description={description}",
        "-f", f"private={private}",
        "-f", f"auto_init=true"
    ]
    
    # 使用token
    env = os.environ.copy()
    env["GH_TOKEN"] = token
    
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, 
            env=env, timeout=30
        )
        if result.returncode == 0:
            return {"status": "success", "data": json.loads(result.stdout)}
        else:
            return {"status": "error", "message": result.stderr}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def push_project(project_path: str, repo_name: str, original_info: dict) -> dict:
    """推送项目到GitHub"""
    token = get_token()
    
    # 添加README致谢内容
    readme_path = os.path.join(project_path, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "a", encoding="utf-8") as f:
            f.write("\n\n---\n")
            f.write("# 致谢\n\n")
            f.write(f"本项目基于 [{original_info.get('name', 'Unknown')}]({original_info.get('url', '')}) 优化而来。\n\n")
            f.write("## 原项目信息\n")
            f.write(f"- **原作者**: {original_info.get('owner', 'Unknown')}\n")
            f.write(f"- **原始描述**: {original_info.get('description', '')}\n")
            f.write(f"- **Star数**: {original_info.get('stars', 'N/A')}\n")
            f.write(f"- **优化日期**: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write("## 优化内容\n")
            for opt in original_info.get('optimizations', []):
                f.write(f"- {opt}\n")
    
    # Git操作
    try:
        subprocess.run(["git", "init"], cwd=project_path, check=True)
        subprocess.run(["git", "add", "."], cwd=project_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"feat: LQ优化版 - {original_info.get('name', '')}"],
            cwd=project_path, check=True
        )
        
        remote_url = f"https://{token}@github.com/{LIQIAN_CONFIG['username']}/{repo_name}.git"
        subprocess.run(
            ["git", "remote", "add", "origin", remote_url],
            cwd=project_path, check=True
        )
        subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=project_path, check=True
        )
        
        return {"status": "success", "url": f"https://github.com/{LIQIAN_CONFIG['username']}/{repo_name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    parser = argparse.ArgumentParser(description="上传优化项目到李迁GitHub")
    parser.add_argument("--project", required=True, help="项目路径")
    parser.add_argument("--name", required=True, help="原始项目名称")
    parser.add_argument("--description", default="LQ优化版项目", help="仓库描述")
    parser.add_argument("--private", action="store_true", help="设为私有仓库")
    parser.add_argument("--original-url", default="", help="原始项目URL")
    parser.add_argument("--original-owner", default="Unknown", help="原始项目作者")
    parser.add_argument("--original-stars", default="N/A", help="原始项目Star数")
    parser.add_argument("--optimizations", nargs="+", default=[], help="优化内容列表")
    
    args = parser.parse_args()
    
    # 添加LQ前缀
    lq_name = f"LQ{args.name}"
    
    original_info = {
        "name": args.name,
        "url": args.original_url,
        "owner": args.original_owner,
        "stars": args.original_stars,
        "description": args.description.replace("LQ优化版 - ", ""),
        "optimizations": args.optimizations
    }
    
    print(f"正在创建仓库: {lq_name}")
    
    # 创建仓库
    result = create_repo(lq_name, args.description, args.private)
    
    if result["status"] == "success":
        print(f"✅ 仓库创建成功: {result['data'].get('html_url')}")
        
        # 推送项目
        push_result = push_project(args.project, lq_name, original_info)
        if push_result["status"] == "success":
            print(f"✅ 项目推送成功: {push_result['url']}")
        else:
            print(f"❌ 推送失败: {push_result['message']}")
    else:
        print(f"❌ 创建失败: {result['message']}")
        print(f"\n💡 请配置李迁的GitHub Token:")
        print(f"   export {LIQIAN_CONFIG['token_env']}=\"<your-token>\"")
        print(f"   然后重新运行此脚本")

if __name__ == "__main__":
    main()
