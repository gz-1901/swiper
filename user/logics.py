import os
import time
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache

from common import utils, cache_keys, config
from libs import sms, qiniuyun
from worker import celery_app


def send_verify_code(phone_num):
    """
    发送验证码逻辑
    :param phone_num: 手机号
    :return: 
    """

    # 生成验证码
    code = utils.gen_rendom_code(6)

    # 发送验证码
    ret = sms.send_verify_code(phone_num, code)

    if ret:
        cache.set(cache_keys.VERIFY_CODE_KEY_PREFIX.format(phone_num), code, 60 * 3)

    return ret


def upload_avatar(file_name, avatar):
    """
    用户上传文件保存之本地服务器
    :param file_name:
    :param avatar:
    :return:
    """
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    with open(file_path, 'wb+') as destination:
        for chunk in avatar.chunks():
            destination.write(chunk)

    return file_path


def upload_qiniuyun(file_name, file_path):
    """
    本地文件上传到七牛云
    :param file_name:
    :param file_path:
    :return:
    """
    ret, info = qiniuyun.upload(file_name, file_path)

    return True if info.status_code == 200 else False


@celery_app.task
def async_upload_avatar(user, avatar):
    """
    异步上传头像到七牛云
    :param avatar:
    :return:
    """
    file_name = 'avatar-{}'.format(int(time.time()))

    file_path = upload_avatar(file_name, avatar)

    ret = upload_qiniuyun(file_name, file_path)

    if ret:
        user.avatar = urljoin(config.QN_HOST, file_name)
        user.save()
