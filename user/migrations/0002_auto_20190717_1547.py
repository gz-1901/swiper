# Generated by Django 2.2.3 on 2019-07-17 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[('gz', '广州'), ('bj', '北京'), ('sz', '深圳'), ('sh', '上海'), ('hz', '杭州'), ('cd', '成都')], default='gz', max_length=16)),
                ('min_distance', models.IntegerField(default=0)),
                ('max_distance', models.IntegerField(default=10)),
                ('min_dating_age', models.IntegerField(default=18)),
                ('max_dating_age', models.IntegerField(default=81)),
                ('dating_sex', models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0)),
                ('auto_play', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'profiles',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0),
        ),
    ]