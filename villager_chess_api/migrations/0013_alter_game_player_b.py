# Generated by Django 4.2.1 on 2023-06-09 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('villager_chess_api', '0012_remove_game_b_notes_remove_game_w_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player_b',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_as_black', to='villager_chess_api.player'),
        ),
    ]
