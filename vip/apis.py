from libs.http import render_json
from vip.models import Vip


def info(request):
    from django.core.cache import cache
    key = 'vip_info'

    vip_info = cache.get(key)

    if vip_info:
        return render_json(data=vip_info)

    vip_info = []

    for vip in Vip.objects.exclude(level=0).order_by('level'):
        v_info = vip.to_dict()
        v_info['perms'] = []

        for perm in vip.perms:
            v_info['perms'].append(perm.to_dict())

        vip_info.append(v_info)

    cache.set(key, vip_info)

    return render_json(data=vip_info)
