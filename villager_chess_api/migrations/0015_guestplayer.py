# Generated by Django 4.2.2 on 2023-06-28 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('villager_chess_api', '0014_game_computer_opponent_alter_game_player_w'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]