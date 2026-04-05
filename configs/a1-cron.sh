#!/bin/bash
# A1 专业能力学习任务 Cron配置
# 每天04:00-07:00自动运行，专注战略规划、行业研究、OpenClaw服务优化
# 学习完成后形成结构化报告

export PATH=/usr/local/bin:/usr/bin:/bin:$PATH
export PYTHONPATH=/root/workspace/software-team/configs:$PYTHONPATH

LOG_DIR="/root/workspace/software-team/logs"
REPORT_DIR="/root/.openclaw/workspace/memory/a1_learn/reports"
LOG_FILE="$LOG_DIR/a1_learn_$(date +\%Y\%m\%d).log"

mkdir -p $LOG_DIR $REPORT_DIR

echo "========== $(date) ==========" >> $LOG_FILE

hour=$(date +%H)

if [ "$hour" -ge "04" ] && [ "$hour" -lt "07" ]; then
    echo "[$(date)] 进入A1专业能力学习模式..." >> $LOG_FILE

    cd /root/workspace/software-team/configs
    python3 a1-cron.py >> $LOG_FILE 2>&1
    PY_EXIT=$?

    echo "[$(date)] 学习完成，退出码: $PY_EXIT" >> $LOG_FILE

    # 提取最新报告摘要
    LATEST_MD="$REPORT_DIR/LATEST.md"
    if [ -f "$LATEST_MD" ]; then
        echo "" >> $LOG_FILE
        echo "========== A1学习报告摘要 ==========" >> $LOG_FILE
        head -20 "$LATEST_MD" >> $LOG_FILE
    fi
else
    echo "[$(date)] 非学习时间(04:00-07:00)，跳过" >> $LOG_FILE
fi
