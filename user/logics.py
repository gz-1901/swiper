from django.core.cache import cache

from common import utils, cache_keys
from libs import sms


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
