from common import errors
from libs.http import render_json
from social import logics
from social.models import Swiped


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

    Swiped.swipe(uid=user.id, sid=sid, mark='dislike')

    return render_json()


def rewind(request):
    return None


def liked_me(request):
    return None
