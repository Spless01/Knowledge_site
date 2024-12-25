# Generated by Django 5.1.4 on 2024-12-20 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0005_alter_article_author_alter_article_doi_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScienceField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('issn_print', models.CharField(blank=True, max_length=20, null=True)),
                ('issn_online', models.CharField(blank=True, max_length=20, null=True)),
                ('link', models.URLField(blank=True, max_length=500, null=True)),
                ('science_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='knowledge.sciencefield')),
            ],
        ),
    ]
