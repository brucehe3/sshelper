# Generated by Django 2.0.6 on 2018-06-28 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180628_1053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercasestep',
            options={'ordering': ['sort_order'], 'verbose_name': '用例步骤', 'verbose_name_plural': '用例步骤管理'},
        ),
        migrations.RenameField(
            model_name='usercasestep',
            old_name='order',
            new_name='sort_order',
        ),
    ]