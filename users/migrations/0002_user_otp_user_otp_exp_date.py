# Generated by Django 4.0 on 2022-02-22 17:42

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="otp",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="otp"),
        ),
        migrations.AddField(
            model_name="user",
            name="otp_exp_date",
            field=models.DateTimeField(blank=True, null=True, verbose_name="otp valid to"),
        ),
        migrations.AddField(
            model_name="user",
            name="invalid_otp_entered",
            field=models.PositiveSmallIntegerField(
                blank=True,
                default=0,
                null=True,
                validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(0)],
                verbose_name="invalid otp entered",
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=False, max_length=64, unique=True, verbose_name='phone'),
        ),
    ]
