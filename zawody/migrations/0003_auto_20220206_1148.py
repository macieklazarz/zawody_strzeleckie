# Generated by Django 3.2.9 on 2022-02-06 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zawody', '0002_auto_20220206_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='konkurencja',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='turniej',
            name='nazwa',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='turniej',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]