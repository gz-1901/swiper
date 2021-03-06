import datetime

from django.core.cache import cache

from common import cache_keys, errors, config
from libs.cache import rds
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
    if ret:
        # 如果滑动成功，则进行滑动积分更新操作
        update_swipe_score(sid, 'like')
        if Swiped.is_liked(sid, uid):
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
    if ret:
        update_swipe_score(sid, 'superlike')
        if Swiped.is_liked(sid, uid):
            # Friend.make_friends(sid, uid)
            _, created = Friend.objects.make_friends(sid, uid)
            return created
    else:
        return False


def rewind(user):
    """
    撤销上一次滑动操作记录
    撤销上一次创建的好友关系
    :param user:
    :return:
    """
    key = cache_keys.SWIPE_LIMIT_PREFIX.format(user.id)

    swipe_times = cache.get(key, 0)

    if swipe_times >= config.SWIPE_LIMIT:
        raise errors.SwipeLimitError

    swipe = Swiped.objects.filter(uid=user.id).latest('created_at')

    if swipe.mark in ['like', 'superlike']:
        Friend.cancel_friends(swipe.uid, swipe.sid)

    swipe.delete()

    now = datetime.datetime.now()
    timeout = 86400 - now.hour * 3600 - now.minute * 60 - now.second

    cache.set(key, swipe_times + 1, timeout=timeout)


def liked_me(user):
    """
    查看喜欢过我的人，过滤掉已经存在的好友
    :param user:
    :return:
    """
    friend_list = Friend.friend_list(user.id)
    swipe_list = Swiped.objects.filter(sid=user.id, mark__in=['like', 'superlike']). \
        exclude(uid__in=friend_list).only('uid')

    liked_me_uid_list = [s.uid for s in swipe_list]

    return liked_me_uid_list


def update_swipe_score(sid, mark):
    score = config.SWIPE_SCORES.get(mark, 0)

    rds.zincrby(cache_keys.HOT_RANK, score, sid)


def get_top_rank(num):
    origin_data = rds.zrevrange('hot_rank', 0, num - 1, withscores=True)
    rank_data = [[int(uid), int(score)] for uid, score in origin_data]

    user_rank = []

    # 单个获取用户数据
    # for uid, score in rank_data:
    #     user = User.get(pk=uid)
    #     user_dict = user.to_dict()
    #     user_dict['score'] = score
    #
    #     user_rank.append(user_dict)

    # # 批量获取用户数据
    uid_list = [uid for uid, _ in rank_data]

    users = User.objects.filter(id__in=uid_list)

    sorted_users = sorted(users, key=lambda user: uid_list.index(user.id))

    for user, (_, score) in zip(sorted_users, rank_data):
        user_dict = user.to_dict()
        user_dict['score'] = score

        user_rank.append(user_dict)

    return user_rank
