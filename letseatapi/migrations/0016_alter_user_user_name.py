# Generated by Django 4.1.3 on 2024-09-10 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letseatapi', '0015_alter_user_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(default='default_user_1725940672', max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
