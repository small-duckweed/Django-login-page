# Generated by Django 2.1.4 on 2019-01-17 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女'), ('unknown', '未知')], default='unknown', max_length=10, verbose_name='性别'),
        ),
    ]
