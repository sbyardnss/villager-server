# Generated by Django 4.2.2 on 2023-06-28 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('villager_chess_api', '0015_guestplayer'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestplayer',
            name='name',
            field=models.CharField(default='Bob Ross', max_length=50),
        ),
    ]