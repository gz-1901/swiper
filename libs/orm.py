from django.core.cache import cache

from common import cache_keys


class ModelToDictMixin():
    def to_dict(self, exclude=None):
        if exclude is None:
            exclude = []

        attr_dict = {}
        fields = self._meta.fields

        for field in fields:
            field_name = field.attname
            if field_name not in exclude:
                attr_dict[field_name] = getattr(self, field_name)

        return attr_dict


"""

user = User.get(pk)

user.save()

"""


@classmethod
def get(cls, *args, **kwargs):
    """
    为 objects 管理增加缓存层

    User.get(pk=123)
    User.get(phonenum=13888888888)

    :param cls:
    :param args:
    :param kwargs:
    :return:
    """

    # 1、从缓存中获得数据
    if 'pk' in kwargs:
        pk = kwargs['pk']
    elif 'id' in kwargs:
        pk = kwargs['id']
    else:
        pk = None

    if pk is not None:
        # key = 'model:User:123456'
        key = cache_keys.MODEL_PERFIX.format(cls.__name__, pk)
        model_obj = cache.get(key)

        if isinstance(model_obj, cls):
            return model_obj

    # 2、如果缓存中不存在，则从数据库中获得数据
    model_obj = cls.objects.get(*args, **kwargs)

    # 3、将数据更新至缓存
    key = cache_keys.MODEL_PERFIX.format(cls.__name__, model_obj.pk)
    cache.set(key, model_obj)

    return model_obj


@classmethod
def get_or_create(cls, defaults=None, **kwargs):
    """

    User.get_or_create(pk=123, phonenum=8645678)

    :param cls:
    :param defaults:
    :param kwargs:
    :return:
    """

    # 1、从缓存中获得数据
    if 'pk' in kwargs:
        pk = kwargs['pk']
    elif 'id' in kwargs:
        pk = kwargs['id']
    else:
        pk = None

    if pk is not None:
        # key = 'model:User:123456'
        key = cache_keys.MODEL_PERFIX.format(cls.__name__, pk)
        model_obj = cache.get(key)

        if isinstance(model_obj, cls):
            return model_obj, False

    # 2、如果缓存中不存在，则从数据库中获得数据
    model_obj, created = cls.objects.get_or_create(defaults=None, **kwargs)

    # 3、将数据更新至缓存
    key = cache_keys.MODEL_PERFIX.format(cls.__name__, model_obj.pk)
    cache.set(key, model_obj)

    return model_obj, created
