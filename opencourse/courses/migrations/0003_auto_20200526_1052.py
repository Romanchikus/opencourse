# Generated by Django 3.0.5 on 2020-05-26 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20200519_0930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='name_ar',
        ),
        migrations.RemoveField(
            model_name='courseage',
            name='name_ar',
        ),
        migrations.RemoveField(
            model_name='coursearea',
            name='name_ar',
        ),
        migrations.RemoveField(
            model_name='courselanguage',
            name='name_ar',
        ),
        migrations.RemoveField(
            model_name='courselevel',
            name='name_ar',
        ),
        migrations.RemoveField(
            model_name='courselocationtype',
            name='name_ar',
        ),
    ]
