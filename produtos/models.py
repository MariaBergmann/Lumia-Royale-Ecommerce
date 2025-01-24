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

from django.conf import settings
import os
from PIL import Image
from django.db import models
from django.utils.text import slugify
from utils import utils


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255, verbose_name= 'Descrição curta')
    descricao_longa = models.TextField(verbose_name= 'Descrição longa')
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m/',
        blank=True,
        null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name= 'Valor Original')
    preco_marketing_promocional = models.FloatField(default=0, verbose_name= 'Valor Promocional')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    def get_preco_formatado(self):
        return f'R${self.preco_marketing: .2f}'.replace('.', ',')
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional_formatado(self):
        return f'R${self.preco_marketing_promocional: .2f}'.replace('.', ',')
    get_preco_promocional_formatado.short_description = 'Promoção'



    @staticmethod
    def resize_image(img, new_width=800):
        # Caminho completo da imagem
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)

        # Dimensões originais da imagem
        original_width, original_height = img_pil.size

        # Verifica se a largura da imagem já é menor ou igual ao limite
        if original_width <= new_width:
            img_pil.close()
            return

        # Calcula a nova altura proporcional à largura
        new_height = round((new_width * original_height) / original_width)

        # Redimensiona a imagem
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)

        # Salva a imagem redimensionada no mesmo caminho
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

        img_pil.close()

    """
    Gerando o Slung automaticamente, Você pode usar a função
    slugify da biblioteca django.utils.text para transformar uma
    string em um slug por exemplo:

    Se você criar um artigo com o título Aprenda Python
    em 10 Passos, o slug será gerado automaticamente como
    aprenda-python-em-10-passos, semm precisar digitar a mão.

    Aqui estamos transformando uma string em um slug.

    """

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slung = slug


        super().save(*args, **kwargs)

        # Largura máxima da imagem
        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)
            def __str__(self):
                return self.nome


class Variacao(models.Model):
        produto = models.ForeignKey("Produto", on_delete=models.CASCADE)
        nome = models.CharField(max_length=50, blank=True, null=True)
        preco = models.FloatField(verbose_name= 'Valor Original')
        preco_promocional = models.FloatField(default=0, verbose_name= 'Valor Promocional')
        estoque = models.PositiveBigIntegerField(default=1)

        def __str__(self):
            return self.nome or self.produto.nome


        class Meta:
          verbose_name = 'Variacao'
          verbose_name_plural = 'Variações'

