import logging
import traceback

from django.utils.deprecation import MiddlewareMixin

from common import errors
from common.errors import LogicException, LogicError
from libs.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        自定义认证中间件

        白名单

        request.path

        根据 request.session['uid'] 来判断登录状态

        :param request:
        :return:
        """
        WHITE_LIST = [
            '/api/vip/info',
            '/api/user/verify-phone',
            '/api/user/login'
        ]

        if request.path in WHITE_LIST:
            return

        uid = request.session.get('uid')

        if not uid:
            return render_json(code=errors.LOGIN_REQUIRED_ERR)

        request.user = User.get(pk=uid)

        # for k,v in request.META.items():
        #     print(k, v)

        # token = request.META.get('HTTP_X_SWIPER_AHTU_TOKEN')
        # uid = cache.get(token)
        #
        # if not uid:
        #     return render_json(code=errors.LOGIN_REQUIRED_ERR)
        #
        # request.user = User.get(pk=uid)


err_logger = logging.getLogger('err')


class LogicExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, (LogicException, LogicError)):
            return render_json(code=exception.code)
        else:
            err_logger.error(traceback.format_exc())
            return render_json(code=errors.ERR)
