import datetime

from social.models import Swiped, Friend
from user.models import User


def recommend_users(user):
    today = datetime.date.today()

    # 18 = 2019 - 2001
    max_year = today.year - user.profile.min_dating_age

    # 22 = 2019 - 1997
    min_year = today.year - user.profile.max_dating_age

    swiped_users = Swiped.objects.filter(uid=user.id).only('sid')
    print(swiped_users.query)
    swiped_sid_list = [s.sid for s in swiped_users]

    rec_users = User.objects.filter(
        location=user.profile.location,
        sex=user.profile.dating_sex,
        birth_year__gte=min_year,
        birth_year__lte=max_year
    ).exclude(id__in=swiped_sid_list)[:20]

    print(rec_users.count())
    print(rec_users.query)

    return rec_users


def like_someone(uid, sid):
    """
    喜欢操作，如果被滑动人，喜欢当前用户，则创建好友关系
    :param uid:
    :param sid:
    :return:
    """
    ret = Swiped.swipe(uid=uid, sid=sid, mark='like')

    # 如果 sid 喜欢 uid，则进行加好友操作
    if ret and Swiped.is_liked(sid, uid):
        _, created = Friend.make_friends(sid, uid)
        # 发送 匹配好友成功的 推送消息
        return created
    else:
        return False


def superlike_someone(uid, sid):
    """
    超级喜欢操作，如果被滑动人，喜欢当前用户，则创建好友关系
    :param uid:
    :param sid:
    :return:
    """
    ret = Swiped.swipe(uid=uid, sid=sid, mark='superlike')

    # 如果 sid 喜欢 uid，则进行加好友操作
    if ret and Swiped.is_liked(sid, uid):
        # Friend.make_friends(sid, uid)
        _, created = Friend.objects.make_friends(sid, uid)
        return created
    else:
        return False
