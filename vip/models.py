from django.db import models

from libs.orm import ModelToDictMixin


class Vip(models.Model, ModelToDictMixin):
    """
    会员
    """
    level = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=128, unique=True)
    # price decimal(5,2)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def perms(self):
        """
        当前 vip  所对应的权限
        :return:
        """
        if not hasattr(self, '_perms'):
            # 通过 vip.id 从 vip-permission 关系表中获得对应的 perm.id
            vip_perms = VipPermission.objects.filter(vip_id=self.id).only('perm_id')
            perms_id_list = [p.perm_id for p in vip_perms]

            # 通过 perm.id 获得 perm
            self._perms = Permission.objects.filter(id__in=perms_id_list)

        return self._perms

    def has_perm(self, perm_name):
        """
        检查当前 vip 是否拥有 某种权限
        :param perm_name:
        :return:
        """
        perm_names = [p.name for p in self.perms]

        return perm_name in perm_names

    class Meta:
        db_table = 'vips'


class Permission(models.Model, ModelToDictMixin):
    """
    权限
    """
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=512)

    class Meta:
        db_table = 'permissions'


class VipPermission(models.Model):
    """
    会员，权限 关系表
    """
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()

    class Meta:
        db_table = 'vip_permissions'
