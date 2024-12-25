# Generated by Django 5.1.4 on 2024-12-20 20:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0007_galuznauki_vidannya_delete_journal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vidannya',
            name='link',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='vidannya',
            name='galuz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge.galuznauki'),
        ),
        migrations.AlterField(
            model_name='vidannya',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]