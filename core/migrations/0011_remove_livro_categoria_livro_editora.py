# Generated by Django 5.1.7 on 2025-05-27 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_livro_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livro',
            name='categoria',
        ),
        migrations.AddField(
            model_name='livro',
            name='editora',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='livros', to='core.editora'),
        ),
    ]
