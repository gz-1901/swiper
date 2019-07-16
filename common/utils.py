import random
import re

PHONE_PATTERN = re.compile(r'^1[3-9]\d{9}$')


def is_phone_num(phone_num):
    """
    验证手机号码格式
    :param phone_num:
    :return:
    """
    return True if PHONE_PATTERN.match(phone_num.strip()) else False


def gen_rendom_code(length=4):
    if not isinstance(length, int):
        length = 1

    if length <= 0:
        length = 1

    code = random.randrange(10 ** (length - 1), 10 ** length)

    return str(code)
