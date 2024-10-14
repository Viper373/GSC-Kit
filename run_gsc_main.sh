#!/bin/bash

# =============================================================================
# Script Name: run_gsc_main.sh
# Description: 检查是否有 GSC cookies，有则运行 gsc_main.py，确保单实例运行
# =============================================================================

# ------------------------------ 配置部分 -----------------------------------
MAIN_SCRIPT="gsc_main.py"
PROJECT_DIR="/app/product/td_gsc_bot"
PROJECT_NAME="td_gsc_bot"
PYTHON_CMD="python"  # 根据实际环境调整，如使用 python3 或指定虚拟环境中的 python

# 获取当前日期
CURRENT_DATE=$(date '+%Y-%m-%d')

# 定义日志目录和文件
LOG_DIR="$PROJECT_DIR/logs/$CURRENT_DATE"
SCRIPT_NAME=$(basename "$0" .sh)
LOG_FILE="$LOG_DIR/${SCRIPT_NAME}_sh.log"

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
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local console_message="${GREEN}${INFO_EMOJI} [INFO] $timestamp - $1${NC}"
    local file_message="${INFO_EMOJI} [INFO] $timestamp - $1"
    echo -e "$console_message"
    echo -e "$file_message" >> "$LOG_FILE"
}

log_success() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local console_message="${GREEN}${SUCCESS_EMOJI} [SUCCESS] $timestamp - $1${NC}"
    local file_message="${SUCCESS_EMOJI} [SUCCESS] $timestamp - $1"
    echo -e "$console_message"
    echo -e "$file_message" >> "$LOG_FILE"
}

log_error() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local console_message="${RED}${ERROR_EMOJI} [ERROR] $timestamp - $1${NC}"
    local file_message="${ERROR_EMOJI} [ERROR] $timestamp - $1"
    echo -e "$console_message"
    echo -e "$file_message" >> "$LOG_FILE"
}

log_warning() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local console_message="${YELLOW}${WARNING_EMOJI} [WARNING] $timestamp - $1${NC}"
    local file_message="${WARNING_EMOJI} [WARNING] $timestamp - $1"
    echo -e "$console_message"
    echo -e "$file_message" >> "$LOG_FILE"
}

# ------------------------------ 主函数 -------------------------------------
run_gsc_main() {
    # 创建日志文件
    if [ ! -d "$LOG_FILE" ]; then
        mkdir -p "$LOG_DIR"
        touch "$LOG_FILE"
    fi

    log_info "开始检查 redis GSC cookies..."

    # 切换到项目目录
    if cd "$PROJECT_DIR"; then
        log_info "切换到目录 \"$PROJECT_DIR\""
    else
        log_error "无法切换到目录 \"$PROJECT_DIR\""
        exit 1
    fi

    # 如果需要激活虚拟环境，可以在这里添加
    source /etc/profile
    source /root/miniconda3/etc/profile.d/conda.sh
    conda activate $PROJECT_NAME

    # 运行主脚本
    nohup $PYTHON_CMD -u $MAIN_SCRIPT >> /dev/null 2>&1 &

    log_success "已启动 \"$MAIN_SCRIPT\""
}

# ------------------------------ 脚本执行入口 -------------------------------
run_gsc_main
