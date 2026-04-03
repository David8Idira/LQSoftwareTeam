#!/bin/bash
# 软件实施团队 - 凌晨学习任务 Cron配置
# 每天00:30-06:00自动运行，学习GitHub热门项目并优化

# 设置环境变量
export PATH=/usr/local/bin:/usr/bin:/bin:$PATH
export PYTHONPATH=/root/workspace/software-team:$PYTHONPATH

# 日志文件
LOG_FILE="/root/workspace/software-team/logs/team_$(date +\%Y\%m\%d).log"

# 创建日志目录
mkdir -p /root/workspace/software-team/logs

echo "========== $(date) ==========" >> $LOG_FILE

# 检查是否在凌晨学习窗口 (00:30 - 06:00)
hour=$(date +%H)
minute=$(date +%M)

if [ "$hour" = "00" ] && [ "$minute" -ge "30" ] || [ "$hour" -ge "01" ] && [ "$hour" -lt "06" ]; then
    echo "[$(date)] 进入学习模式..." >> $LOG_FILE
    
    # 运行Python团队脚本
    cd /root/workspace/software-team
    python3 software_team.py >> $LOG_FILE 2>&1
    
    echo "[$(date)] 学习完成" >> $LOG_FILE
else
    echo "[$(date)] 非学习时间，检查待处理任务..." >> $LOG_FILE
fi
