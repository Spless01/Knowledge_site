# Generated by Django 5.1.4 on 2024-12-30 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0012_journal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='title',
            field=models.CharField(max_length=1000),
        ),
    ]