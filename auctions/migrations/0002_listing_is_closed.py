# Generated by Django 3.2.2 on 2021-07-09 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
