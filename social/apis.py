from common import errors
from libs.cache import rds
from libs.http import render_json
from social import logics
from social.models import Swiped
from social.permissions import has_perm
from user.models import User


def recommend(request):
    user = request.user

    rec_users = logics.recommend_users(user)

    users = [u.to_dict() for u in rec_users]

    return render_json(data=users)


def like(request):
    user = request.user
    sid = request.POST.get('sid')

    if sid is None:
        return render_json(code=errors.SID_ERR)

    sid = int(sid)

    matched = logics.like_someone(user.id, sid)

    return render_json(data={'matched': matched})


@has_perm('superlike')
def superlike(request):
    user = request.user
    sid = request.POST.get('sid')

    if sid is None:
        return render_json(code=errors.SID_ERR)

    sid = int(sid)

    matched = logics.superlike_someone(user.id, sid)

    return render_json(data={'matched': matched})


def dislike(request):
    user = request.user
    sid = request.POST.get('sid')

    if sid is None:
        return render_json(code=errors.SID_ERR)

    sid = int(sid)

    ret = Swiped.swipe(uid=user.id, sid=sid, mark='dislike')

    if ret:
        logics.update_swipe_score(sid, 'dislike')

    return render_json()


@has_perm('rewind')
def rewind(request):
    """
    反悔接口
    :param request:
    :return:
    """
    user = request.user

    logics.rewind(user)

    return render_json()


@has_perm('liked_me')
def liked_me(request):
    user = request.user

    uid_list = logics.liked_me(user)

    users = [u.to_dict() for u in User.objects.filter(id__in=uid_list)]

    return render_json(data=users)


def top_rank(request):

    user_rank = logics.get_top_rank(10)

    return render_json(data=user_rank)