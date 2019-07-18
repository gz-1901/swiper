from libs.http import render_json
from social import logics


def recommend(request):
    user = request.user

    rec_users = logics.recommend_users(user)

    users = [u.to_dict() for u in rec_users]

    return render_json(data=users)


def like(request):
    user = request.user
    sid = request.POST.get('sid')

    logics.like_someone(user.id, sid)

    return render_json()


def dislike(request):
    return None


def superlike(request):
    return None


def rewind(request):
    return None


def liked_me(request):
    return None
