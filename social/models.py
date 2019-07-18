from django.db import models


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

    class Meta:
        db_table = 'swiped'
