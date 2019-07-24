#!/bin/bash

PROJECT_DIR='/opt/swiper'

cd $PROJECT_DIR
source .venv/bin/activate
gunicorn -c swiper/gunicorn-config.py swiper.wsgi
deactivate
