import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_itenscompra_preco'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autor',
            options={'verbose_name': 'autor', 'verbose_name_plural': 'autores'},
        ),
        migrations.AddField(
            model_name='compra',
            name='data',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='compra',
            name='tipo_pagamento',
            field=models.IntegerField(choices=[(1, 'Cartão de Crédito'), (2, 'Cartão de Débito'), (3, 'PIX'), (4, 'Boleto'), (5, 'Transferência Bancária'), (6, 'Dinheiro'), (7, 'Outro')], default=1),
        ),
        migrations.AddField(
            model_name='compra',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='autor',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='autor',
            name='nome',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='itenscompra',
            name='livro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='itenscompra', to='core.livro'),
        ),
        migrations.AlterField(
            model_name='itenscompra',
            name='preco',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='livro',
            name='preco',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
