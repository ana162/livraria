# Generated by Django 5.1.7 on 2025-05-23 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_livro_autores_livro_categoria_livro_editora'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livro',
            name='autores',
        ),
        migrations.RemoveField(
            model_name='livro',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='livro',
            name='editora',
        ),
    ]
