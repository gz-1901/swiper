from common import errors


def has_perm(perm_name):
    def decorator(view_func):
        def wapper(request, *args, **kwargs):
            if request.user.vip.has_perm(perm_name):
                return view_func(request, *args, **kwargs)
            else:
                raise errors.VipPermError

        return wapper

    return decorator
