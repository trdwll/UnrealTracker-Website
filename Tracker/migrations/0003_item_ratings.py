# Generated by Django 3.1.7 on 2021-04-20 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0002_auto_20210331_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='ratings',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
    ]
