# Generated by Django 4.0 on 2021-12-25 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NYSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion_text', models.CharField(max_length=200)),
                ('submission_date', models.DateTimeField(auto_now=True)),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
    ]
