from django.http import JsonResponse

from common import errors


def render_json(code=errors.OK, data=None):
    """
    json 返回格式

    :param code: 错误码
    :param data: 接口数据
    :return:
    """
    result = {
        'code': code
    }

    if data:
        result['data'] = data

    json_dumps_params = {
        'separators': (',', ':')
    }

    return JsonResponse(data=result, json_dumps_params=json_dumps_params)
