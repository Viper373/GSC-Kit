#!/bin/bash

# =============================================================================
# Script Name: run_gsc_main.sh
# Description: 检查是否有 GSC cookies，有则运行 gsc_main.py，确保单实例运行
# =============================================================================
# shellcheck disable=SC2034
# ------------------------------ 配置部分 -----------------------------------
MAIN_SCRIPT="gsc_main.py"
CHECK_SCRIPT="checks.py"
PROJECT_DIR="/app/product/td_gsc_bot"
PROJECT_NAME="td_gsc_bot"
PYTHON_CMD="python"  # 根据实际环境调整，如使用 python3 或指定虚拟环境中的 python

# ------------------------------ 颜色与 Emoji 定义 ---------------------------
# 定义颜色变量
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # 无颜色

# 定义 Emoji 变量
INFO_EMOJI="♻️"
WARNING_EMOJI="⚠️"
SUCCESS_EMOJI="✅"
ERROR_EMOJI="❌"
START_EMOJI="▶️"

# ------------------------------ 日志函数 -----------------------------------
log_info() {
    echo -e "${GREEN}${INFO_EMOJI} [INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1${NC}"
}

log_success() {
    echo -e "${GREEN}${SUCCESS_EMOJI} [SUCCESS] $(date '+%Y-%m-%d %H:%M:%S') - $1${NC}"
}

log_error() {
    echo -e "${RED}${ERROR_EMOJI} [ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}${WARNING_EMOJI} [WARNING] $(date '+%Y-%m-%d %H:%M:%S') - $1${NC}"
}

# ------------------------------ 主函数 -------------------------------------
run_gsc_main() {
    log_info "开始检查 GSC cookies..."

    # 切换到项目目录
    if cd "$PROJECT_DIR"; then
        log_info "切换到目录 \"$PROJECT_DIR\""
    else
        log_error "无法切换到目录 \"$PROJECT_DIR\""
        exit 1
    fi

    # 如果需要激活虚拟环境，可以在这里添加
    source /root/miniconda3/etc/profile.d/conda.sh
    conda activate td_gsc_bot

    # 执行检查脚本，获取结果
    CHECK_RESULT=$($PYTHON_CMD "$CHECK_SCRIPT")
    log_info "检查cookies脚本 \"$CHECK_SCRIPT\" 执行完毕"
    CHECK_RESULT=$(echo "$CHECK_RESULT" | tr -d '[:space:]')
    log_info "检查cookies结果: $CHECK_RESULT"

    if [ "$CHECK_RESULT" = "True" ]; then
        log_info "检测到 GSC cookies，启动 \"$MAIN_SCRIPT\""

        # 运行主脚本
        nohup $PYTHON_CMD -u "$MAIN_SCRIPT" >> /dev/null 2>&1 &

        log_success "已启动 \"$MAIN_SCRIPT\""
    else
        log_info "没有 GSC 任务，任务结束"
    fi
}

# ------------------------------ 脚本执行入口 -------------------------------
run_gsc_main
