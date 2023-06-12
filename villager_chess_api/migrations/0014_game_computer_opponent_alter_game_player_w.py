# Generated by Django 4.2.1 on 2023-06-12 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('villager_chess_api', '0013_alter_game_player_b'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='computer_opponent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='game',
            name='player_w',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_as_white', to='villager_chess_api.player'),
        ),
    ]
