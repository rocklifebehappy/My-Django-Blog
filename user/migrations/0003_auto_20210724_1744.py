# Generated by Django 3.2.5 on 2021-07-24 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210724_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
