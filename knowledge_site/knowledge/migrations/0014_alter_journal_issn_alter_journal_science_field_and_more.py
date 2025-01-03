# Generated by Django 5.1.4 on 2024-12-30 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0013_alter_journal_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='issn',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='journal',
            name='science_field',
            field=models.CharField(blank=True, max_length=2550),
        ),
        migrations.AlterField(
            model_name='journal',
            name='specialty',
            field=models.CharField(blank=True, max_length=2550),
        ),
    ]
