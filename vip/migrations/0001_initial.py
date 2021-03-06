# Generated by Django 2.2.3 on 2019-07-22 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'permissions',
            },
        ),
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=128)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
            options={
                'db_table': 'vips',
            },
        ),
        migrations.CreateModel(
            name='VipPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_id', models.IntegerField()),
                ('perm_id', models.IntegerField()),
            ],
            options={
                'db_table': 'vip_permissions',
            },
        ),
    ]
