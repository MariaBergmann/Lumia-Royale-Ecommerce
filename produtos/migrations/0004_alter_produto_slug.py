# Generated by Django 5.1.3 on 2024-11-26 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("produtos", "0003_alter_variacao_options_alter_produto_tipo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produto",
            name="slug",
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
