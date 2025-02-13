# Generated by Django 5.0.6 on 2024-10-30 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamerapp', '0004_game'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='description',
            new_name='summary',
        ),
        migrations.RemoveField(
            model_name='game',
            name='category',
        ),
        migrations.RemoveField(
            model_name='game',
            name='price',
        ),
        migrations.AddField(
            model_name='game',
            name='available_devices',
            field=models.CharField(default='pc', max_length=255),
        ),
        migrations.AddField(
            model_name='game',
            name='genre',
            field=models.CharField(default='action', max_length=100),
        ),
        migrations.AddField(
            model_name='game',
            name='pricing',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(upload_to='game_images/'),
        ),
        migrations.AlterField(
            model_name='game',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='CurrentSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processor', models.CharField(max_length=100)),
                ('ram', models.PositiveIntegerField()),
                ('gpu', models.CharField(max_length=100)),
                ('storage', models.PositiveIntegerField()),
                ('game', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='current_specs', to='gamerapp.game')),
            ],
        ),
        migrations.CreateModel(
            name='RequiredSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processor', models.CharField(max_length=100)),
                ('ram', models.PositiveIntegerField()),
                ('gpu', models.CharField(max_length=100)),
                ('storage', models.PositiveIntegerField()),
                ('game', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='required_specs', to='gamerapp.game')),
            ],
        ),
    ]
