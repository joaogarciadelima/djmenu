# Generated by Django 2.2.7 on 2019-11-24 12:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='active',
            field=models.BooleanField(default=True, verbose_name='ativo'),
        ),
        migrations.AddField(
            model_name='menu',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='criado em'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menu',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modificado em'),
        ),
        migrations.AddField(
            model_name='menucategory',
            name='active',
            field=models.BooleanField(default=True, verbose_name='ativo'),
        ),
        migrations.AddField(
            model_name='menucategory',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='criado em'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menucategory',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modificado em'),
        ),
    ]
