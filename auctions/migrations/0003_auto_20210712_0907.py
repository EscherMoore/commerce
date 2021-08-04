# Generated by Django 3.2.2 on 2021-07-12 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_is_closed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catagory', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='catagory',
            field=models.ManyToManyField(blank=True, related_name='listings', to='auctions.Catagory'),
        ),
    ]