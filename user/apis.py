from django.http import JsonResponse

from common import errors
from common.utils import is_phone_num
from libs.http import render_json
from user import logics


def verify_phone(request):
    """
    # 1、验证手机格式
    # 2、生成验证码
    # 3、保存验证码
    # 4、发送验证码

    :param request:
    :return:
    """
    phone_num = request.POST.get('phone_num')

    if is_phone_num(phone_num):
        # 生成验证码
        # 发送验证码
        if logics.send_verify_code(phone_num):
            return render_json()
        else:
            return render_json(code=errors.SMS_SEND_ERR)
    else:
        return render_json(code=errors.PHONE_NUM_ERR)
