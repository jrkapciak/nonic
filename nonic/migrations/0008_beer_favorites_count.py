# Generated by Django 4.0 on 2022-02-12 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonic', '0007_alter_beer_favorites_alter_beer_users_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='favorites_count',
            field=models.IntegerField(blank=True, default=0, verbose_name='Favorite count'),
        ),
    ]
