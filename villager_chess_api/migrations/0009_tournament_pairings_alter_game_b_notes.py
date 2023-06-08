# Generated by Django 4.2.1 on 2023-06-07 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('villager_chess_api', '0008_tournament_rounds_alter_tournament_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='pairings',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='game',
            name='b_notes',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]