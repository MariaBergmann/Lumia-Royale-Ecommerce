# Importações devem ser feitas no início do arquivo
from django.db import models
from django.contrib.auth.models import User  # Importado para ligar um pedido com o usuário

# Docstring para a classe Pedido
"""
Pedido:
    user - FK User
    total - Float
    status - Choices:
        ('A', 'Aprovado'),
        ('C', 'Criado'),
        ('R', 'Reprovado'),
        ('P', 'Pendente'),
        ('E', 'Enviado'),
        ('F', 'Finalizado'),

"""

# Explicação sobre o uso de ForeignKey e on_delete default e PositiveBigIntegerField
"""
ForeignKey é a chave estrangeira. No contexto do Django, o campo ForeignKey é usado
para definir relacionamentos entre modelos (tabelas), criando uma ligação entre eles.

Defaut em Django é usado para definir um valor padrão para um campo;Preenche automaticamente
campos sem valor,evita erros por campos vazios ou NULL.Torna os modelos mais resilientes a dados
incompletos.

PositiveBigIntegerField é um tipo de campo de modelo usado para armazenar números inteiros,
positivos grandes (semelhante ao BigIntegerField, mas restringindo os valores a serem não
negativos). Ele é útil para garantir que os dados armazenados em uma coluna sejam sempre
inteiros positivos de até 64 bits.

O argumento on_delete define o que acontece quando um registro na tabela referenciada
(User) é deletado:

models.CASCADE: Se o autor for deletado, todos os livros associados a ele também serão deletados.
models.PROTECT: Impede a exclusão do autor se ele tiver livros associados.
models.SET_NULL: Define o valor do campo como NULL caso o autor seja deletado.
models.SET_DEFAULT: Define um valor padrão caso o autor seja deletado.
models.DO_NOTHING: Não faz nada, mas pode causar erros de integridade referencial.

"""

# Classe Pedido
class Pedido(models.Model):

     """
    Classe que representa um pedido de um usuário.
    Contém informações como o usuário responsável, o valor total e o status do pedido.

     """
     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
     total = models.FloatField()
     qtd_total = models.PositiveIntegerField()
     status = models.CharField(
        default="C",  # 'C' de Criado
        max_length=1,  # Apenas uma letra
        choices=(  # Choices é uma tupla de tuplas
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )

     def __str__(self):
        return f'Pedido N. {self.pk}'

# Docstring para a classe ItemPedido
"""
ItemPedido:
    pedido - FK Pedido
    produto - Char
    produto_id - Int
    variacao - Char
    variacao_id - Int
    preco - Float
    preco_promocional - Float
    quantidade - Int
    imagem - Char

"""

# Classe ItemPedido
class ItemPedido(models.Model):

    """
    Classe que representa um item dentro de um pedido.
    Contém informações como o produto, quantidade, preço e outros detalhes relacionados
    ao item do pedido.

    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do {self.pedido}'

    class Meta:

        """
        Ajuste para plural.

        """
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'
