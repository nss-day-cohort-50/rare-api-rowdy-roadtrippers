# Generated by Django 3.2.9 on 2021-11-15 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rareuser',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rareuser',
            name='created_on',
            field=models.DateField(default='2021-11-15'),
            preserve_default=False,
        ),
    ]
