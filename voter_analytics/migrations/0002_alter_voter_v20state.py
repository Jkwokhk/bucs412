# Generated by Django 4.2.16 on 2024-11-12 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='v20state',
            field=models.BooleanField(),
        ),
    ]
