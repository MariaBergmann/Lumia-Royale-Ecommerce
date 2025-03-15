"""   Produto:
        Produto:
            nome - Char
            descricao_curta - Text
            descricao_longa - Text
            imagem - Image
            slug - Slug
            preco_marketing - Float
            preco_marketing_promocional - Float
            tipo - Choices
                ('V', 'Variável'),
                ('S', 'Simples'),

        Variacao:
            nome - char
            produto - FK Produto
            preco - Float
            preco_promocional - Float
            estoque - Int

"""

from django.db import models
from decimal import Decimal
import locale
import os
from PIL import Image
from django.utils.text import slugify
from django.conf import settings

# Configuração de locale para formato brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255, verbose_name='Descrição curta')
    descricao_longa = models.TextField(verbose_name='Descrição longa')
    imagem = models.ImageField(upload_to='produto_imagens/%Y/%m/', blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Valor Original')
    preco_marketing_promocional = models.FloatField(default=0, verbose_name='Valor Promocional')

    slug = models.SlugField(unique=True, blank=True, null=True)  # ADICIONADO

    # Métodos de formatação de preços
    def get_preco_formatado(self):
        return f'R$ {self.preco_marketing:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    def get_preco_promocional_formatado(self):
        return f'R$ {self.preco_marketing_promocional:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    def __str__(self):
        return self.nome

    @staticmethod
    def resize_image(img, new_width=800):
        """Redimensiona a imagem para um novo tamanho."""
        if not img:
            return

        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)

        if not os.path.exists(img_full_path):
            return

        try:
            img_pil = Image.open(img_full_path)
            original_width, original_height = img_pil.size

            if original_width <= new_width:
                img_pil.close()
                return

            new_height = round((new_width * original_height) / original_width)
            new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
            new_img.save(img_full_path, optimize=True, quality=50)
            img_pil.close()
        except Exception as e:
            print(f"Erro ao redimensionar imagem: {e}")

    def save(self, *args, **kwargs):
        """Gera o slug automaticamente ao salvar o produto e redimensiona a imagem."""
        if not self.slug:
            self.slug = slugify(self.nome)

        super().save(*args, **kwargs)

        if self.imagem and self.imagem.name:
            self.resize_image(self.imagem, 800)

class Variacao(models.Model):
    produto = models.ForeignKey("Produto", on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Original')
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Valor Promocional')
    estoque = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

