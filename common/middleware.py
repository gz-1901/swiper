from django.utils.deprecation import MiddlewareMixin


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
        pass
