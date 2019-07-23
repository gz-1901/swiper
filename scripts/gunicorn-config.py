# -*- coding: utf-8 -*-

from multiprocessing import cpu_count

bind = ["127.0.0.1:9000"]  # 线上环境不会开启在公网 IP 下，一般使用内网 IP
daemon = True  # 是否开启守护进程模式
pidfile = 'logs/gunicorn.pid'

workers = cpu_count() * 2  # 工作进程数量
worker_class = "gevent"  # 指定一个异步处理的库
worker_connections = 65535

keepalive = 60  # 服务器保持连接的时间，能够避免频繁的三次握手过程
timeout = 30
graceful_timeout = 10
forwarded_allow_ips = '*'

# 日志处理
capture_output = True
loglevel = 'info'
errorlog = 'logs/gunicorn.log'

raw_env = [
    'DJANGO_SETTINGS_MODULE=swiper.settings'
]