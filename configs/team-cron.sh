#!/bin/bash
# 软件实施团队 - 凌晨学习任务 Cron配置
# 每天00:00-04:00自动运行，学习GitHub热门项目并优化
# 学习完成后生成结构化报告

# 设置环境变量
export PATH=/usr/local/bin:/usr/bin:/bin:$PATH
export PYTHONPATH=/root/workspace/software-team:$PYTHONPATH

# 目录定义
TEAM_DIR="/root/workspace/software-team"
LOG_DIR="$TEAM_DIR/logs"
REPORT_DIR="$TEAM_DIR/learn/reports"

# 日志文件
LOG_FILE="$LOG_DIR/team_$(date +\%Y\%m\%d).log"

# 创建目录
mkdir -p $LOG_DIR $REPORT_DIR

echo "========== $(date) ==========" >> $LOG_FILE

# 检查是否在凌晨学习窗口 (00:30 - 06:00)
hour=$(date +%H)
minute=$(date +%M)

if [ "$hour" = "00" ] || [ "$hour" -ge "01" ] && [ "$hour" -lt "04" ]; then
    echo "[$(date)] 进入学习模式..." >> $LOG_FILE
    
    # 运行Python团队脚本，捕获输出
    cd $TEAM_DIR
    python3 software_team.py >> $LOG_FILE 2>&1
    PY_EXIT=$?
    
    echo "[$(date)] 学习完成，退出码: $PY_EXIT" >> $LOG_FILE
    
    # 查找最新生成的学习报告
    if [ -d "$REPORT_DIR" ]; then
        LATEST_MD=$(ls -t $REPORT_DIR/*.md 2>/dev/null | head -1)
        if [ -n "$LATEST_MD" ] && [ "$LATEST_MD" != "$REPORT_DIR/LATEST.md" ]; then
            REPORT_MD="$REPORT_DIR/LATEST.md"
            echo "" >> $LOG_FILE
            echo "========== 学习报告摘要 ==========" >> $LOG_FILE
            head -30 "$REPORT_MD" >> $LOG_FILE
            echo "报告完整内容: $REPORT_MD" >> $LOG_FILE
        fi
    fi
else
    echo "[$(date)] 非学习时间，检查待处理任务..." >> $LOG_FILE
fi
