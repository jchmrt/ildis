# Generated by Django 4.0 on 2021-12-25 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nysuggestion',
            name='sender_hallway',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nysuggestion',
            name='sender_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
