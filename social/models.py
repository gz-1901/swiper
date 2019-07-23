from django.db import models
from django.db.models import Q

from common import errors
from common.errors import LogicException
from social.managers import FriendManager


class Swiped(models.Model):
    """
    滑动记录
    """
    MARKS = (
        ('like', '喜欢'),
        ('dislike', '不喜欢'),
        ('superlike', '超级喜欢'),
    )

    uid = models.IntegerField()
    sid = models.IntegerField()
    mark = models.CharField(max_length=16, choices=MARKS)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def swipe(cls, uid, sid, mark):
        """
        创建滑动记录，如果已经存在记录，则返回 False，否则 创建记录，返回 True
        :param uid:
        :param sid:
        :param mark:
        :return:
        """
        marks = [m for m, _ in cls.MARKS]

        if mark not in marks:
            # raise LogicException(errors.SWIPE_ERR)
            raise errors.SwipeError

        # cls.objects.update_or_create(uid=uid, sid=sid, mark=mark)

        if cls.objects.filter(uid=uid, sid=sid).exists():
            return False
        else:
            cls.objects.create(uid=uid, sid=sid, mark=mark)
            return True

    @classmethod
    def is_liked(cls, uid, sid):
        return cls.objects.filter(uid=uid, sid=sid, mark__in=['like', 'superlike']).exists()

    class Meta:
        db_table = 'swiped'


class Friend(models.Model):
    """
    好友关系表

    uid     fid
    -------------------
    1       12
    1       23
    2       34
    3       78
    12      1
    23      1
    34      2
    78      3

    uid1    uid2
    -------------------
    1       12
    1       23
    2       34
    3       78

    uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
    """

    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    objects = FriendManager()

    @classmethod
    def make_friends(cls, uid1, uid2):
        """
        建立好友关系

        通过自定义 uid 排序规则，来组织好友关系，且一组好友关系只保存一份数据
        :param uid1:
        :param uid2:
        :return:
        """
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return cls.get_or_create(uid1=uid1, uid2=uid2)

    @classmethod
    def cancel_friends(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)

        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def friend_list(cls, uid):
        fid_list = []
        friends = cls.objects.filter(Q(uid1=uid) | Q(uid2=uid))

        for f in friends:
            fid = f.uid1 if uid == f.uid2 else f.uid2
            fid_list.append(fid)

        return fid_list

    class Meta:
        db_table = 'friends'
