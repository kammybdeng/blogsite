# Generated by Django 3.0.6 on 2020-08-28 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogposts', '0005_auto_20200824_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='title example', max_length=50),
        ),
    ]