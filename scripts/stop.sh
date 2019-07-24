#!/bin/bash

PROJECT_DIR='/opt/swiper'
PIDFILE="$PROJECT_DIR/logs/gunicorn.pid"

if ! kill `cat $PIDFILE`; then
    echo 'Gunicorn终止失败'
fi
