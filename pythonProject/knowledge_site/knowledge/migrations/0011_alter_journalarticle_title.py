# Generated by Django 5.1.4 on 2024-12-25 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0010_alter_journalarticle_title_alter_subtopic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalarticle',
            name='title',
            field=models.CharField(max_length=3000),
        ),
    ]