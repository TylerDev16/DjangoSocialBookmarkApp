# Generated by Django 4.0.6 on 2022-07-22 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0002_alter_action_verb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='verb',
            field=models.CharField(max_length=225),
        ),
    ]