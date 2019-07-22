#!/usr/bin/env python

import os
import sys
import random

import django

# 设置环境
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")
django.setup()


from user.models import User
from vip.models import Vip, Permission, VipPermission


last_names = (
    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨'
    '朱秦尤许何吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
    '鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
    '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常'
    '乐于时傅皮卞齐康伍余元卜顾孟平黄'
)

first_names = {
    '1': [
        '致远', '俊驰', '雨泽', '烨磊', '晟睿',
        '天佑', '文昊', '修洁', '黎昕', '远航',
        '旭尧', '鸿涛', '伟祺', '荣轩', '越泽',
        '浩宇', '瑾瑜', '皓轩', '浦泽', '绍辉',
        '绍祺', '升荣', '圣杰', '晟睿', '思聪'
    ],
    '2': [
        '沛玲', '欣妍', '佳琦', '雅芙', '雨婷',
        '韵寒', '莉姿', '雨婷', '宁馨', '妙菱',
        '心琪', '雯媛', '诗婧', '露洁', '静琪',
        '雅琳', '灵韵', '清菡', '溶月', '素菲',
        '雨嘉', '雅静', '梦洁', '梦璐', '惠茜'
    ]
}


def random_name():
    last_name = random.choice(last_names)
    sex = random.choice(list(first_names.keys()))
    first_name = random.choice(first_names[sex])
    return ''.join([last_name, first_name]), sex


def create_robots(n):
    # 创建初始用户
    for i in range(n):
        name, sex = random_name()
        try:
            User.objects.create(
                phonenum='%s' % random.randrange(21000000000, 21900000000),
                nickname=name,
                sex=int(sex),
                birth_year=random.randint(1980, 2000),
                birth_month=random.randint(1, 12),
                birth_day=random.randint(1, 28),
                location=random.choice(['bj', 'sh', 'sz', 'gz', 'cd', 'hz']),
            )
            print('created: %s %s' % (name, sex))
        except django.db.utils.IntegrityError:
            pass


def init_permission():
    '''创建权限模型'''
    permissions = (
        ('vipflag',       '会员身份标识'),
        ('superlike',     '超级喜欢'),
        ('rewind',        '反悔功能'),
        ('anylocation',   '任意更改定位'),
        ('unlimit_like',  '无限喜欢次数'),
        ('liked_me', '查看喜欢过我的人'),
    )

    for name, desc in permissions:
        perm, _ = Permission.objects.get_or_create(name=name, description=desc)

        print('create permission %s' % perm.name)


def init_vip():
    for i in range(4):
        vip, _ = Vip.objects.get_or_create(
            name='%d 级会员' % i,
            level=i,
            price=i * 5.0
        )
        print('create %s' % vip.name)


def create_vip_perm_relations():
    '''创建 Vip 和 Permission 的关系'''
    # 获取 VIP
    vip1 = Vip.objects.get(level=1)
    vip2 = Vip.objects.get(level=2)
    vip3 = Vip.objects.get(level=3)

    # 获取权限
    vipflag = Permission.objects.get(name='vipflag')
    superlike = Permission.objects.get(name='superlike')
    rewind = Permission.objects.get(name='rewind')
    anylocation = Permission.objects.get(name='anylocation')
    unlimit_like = Permission.objects.get(name='unlimit_like')
    show_liked_me = Permission.objects.get(name='liked_me')

    # 给 VIP 1 分配权限
    VipPermission.objects.get_or_create(vip_id=vip1.id, perm_id=vipflag.id)
    VipPermission.objects.get_or_create(vip_id=vip1.id, perm_id=superlike.id)

    # 给 VIP 2 分配权限
    VipPermission.objects.get_or_create(vip_id=vip2.id, perm_id=vipflag.id)
    VipPermission.objects.get_or_create(vip_id=vip2.id, perm_id=superlike.id)
    VipPermission.objects.get_or_create(vip_id=vip2.id, perm_id=rewind.id)

    # 给 VIP 3 分配权限
    VipPermission.objects.get_or_create(vip_id=vip3.id, perm_id=vipflag.id)
    VipPermission.objects.get_or_create(vip_id=vip3.id, perm_id=superlike.id)
    VipPermission.objects.get_or_create(vip_id=vip3.id, perm_id=rewind.id)
    VipPermission.objects.get_or_create(vip_id=vip3.id, perm_id=anylocation.id)
    VipPermission.objects.get_or_create(vip_id=vip3.id, perm_id=unlimit_like.id)
    VipPermission.objects.get_or_create(vip_id=vip3.id, perm_id=show_liked_me.id)


if __name__ == '__main__':
    # create_robots(2000)
    init_permission()
    init_vip()
    create_vip_perm_relations()
