#!/bin/bash

PROJECT_DIR='/opt/swiper'
LOGFILE="$PROJECT_DIR/logs/celery.log"

cd $PROJECT_DIR
source .venv/bin/activate

# 为 celery 设置 root 身份
export C_FORCE_ROOT=1
# 将 celery 运行在后台，并将日志写入 celery.log 文件
nohup celery worker -A worker --loglevel=info &>$LOGFILE&

deactivate
