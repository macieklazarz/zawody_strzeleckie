# Generated by Django 3.2.9 on 2022-02-06 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wyniki', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wyniki',
            name='slug',
            field=models.SlugField(default='1'),
            preserve_default=False,
        ),
    ]
