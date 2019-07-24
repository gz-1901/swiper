#!/bin/bash

LOCAL_DIR='./'
REMOTE_DIR='/opt/swiper'

USER='root'
HOST='35.194.171.19'

rsync -crvP --delete --exclude={.git,.venv,logs,__pycache__} $LOCAL_DIR $USER@$HOST:$REMOTE_DIR/

# 远程重启
ssh $USER@$HOST "$REMOTE_DIR/scripts/restart.sh"
