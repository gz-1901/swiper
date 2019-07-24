#!/bin/bash

PROJECT_DIR='/opt/swiper'
PIDFILE="$PROJECT_DIR/logs/gunicorn.pid"

# 简单粗暴
# $PROJECT_DIR/scripts/stop.sh
# $PROJECT_DIR/scripts/start.sh

# 平滑重启
if ! kill -HUP `cat $PIDFILE`; then
    # 如果重启失败，说明服务器已经挂掉，直接启动即可
    $PROJECT_DIR/scripts/start.sh
fi
