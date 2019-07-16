from common import utils
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
    return sms.send_verify_code(phone_num, code)
