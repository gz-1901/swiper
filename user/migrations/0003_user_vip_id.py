# Generated by Django 2.2.3 on 2019-07-22 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190717_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='vip_id',
            field=models.IntegerField(default=1),
        ),
    ]
