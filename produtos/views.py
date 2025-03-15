from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

from . import models
from perfil.models import Perfil


class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 9  # quantidade de itens por página
    ordering = ['-id']


class Busca(ListaProdutos):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session.get('termo', '')
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs

        self.request.session['termo'] = termo
        self.request.session.save()

        return qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produtos'
    slug_url_kwarg = 'slug'


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produtos:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto não existe')
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = float(variacao.preco)  # Convertido para float
        preco_unitario_promocional = float(variacao.preco_promocional) if variacao.preco_promocional else None
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem.name if produto.imagem else ''

        if variacao_estoque < 1:
            messages.error(self.request, 'Estoque insuficiente')
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade'] + 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                    f'no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = (
                preco_unitario_promocional * quantidade_carrinho if preco_unitario_promocional else None
            )
        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu '
            f'carrinho {carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produtos:lista')
        )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id or not self.request.session.get('carrinho'):
            return redirect(http_referer)

        carrinho = self.request.session['carrinho']

        if variacao_id not in carrinho:
            return redirect(http_referer)

        messages.success(
            self.request,
            f'Produto {carrinho[variacao_id]["produto_nome"]} {carrinho[variacao_id]["variacao_nome"]} '
            f'removido do seu carrinho.'
        )

        del carrinho[variacao_id]
        self.request.session.save()
        return redirect(http_referer)


class Carrinho(View):
    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho', {})

        # Convertendo os preços para float antes de passar ao template
        for item in carrinho.values():
            item['preco_unitario'] = float(item['preco_unitario'])
            item['preco_unitario_promocional'] = float(item['preco_unitario_promocional']) if item['preco_unitario_promocional'] else None
            item['preco_quantitativo'] = float(item['preco_quantitativo'])
            item['preco_quantitativo_promocional'] = float(item['preco_quantitativo_promocional']) if item['preco_quantitativo_promocional'] else None

        contexto = {
            'carrinho': carrinho
        }

        return render(self.request, 'produto/carrinho.html', contexto)


class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        if not Perfil.objects.filter(usuario=self.request.user).exists():
            messages.error(self.request, 'Usuário sem perfil.')
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho vazio.')
            return redirect('produto:lista')

        carrinho = self.request.session['carrinho']

        # Convertendo os preços para float antes de passar ao template
        for item in carrinho.values():
            item['preco_unitario'] = float(item['preco_unitario'])
            item['preco_unitario_promocional'] = float(item['preco_unitario_promocional']) if item['preco_unitario_promocional'] else None
            item['preco_quantitativo'] = float(item['preco_quantitativo'])
            item['preco_quantitativo_promocional'] = float(item['preco_quantitativo_promocional']) if item['preco_quantitativo_promocional'] else None

        contexto = {
            'usuario': self.request.user,
            'carrinho': carrinho,
        }

        return render(self.request, 'produto/resumodacompra.html', contexto)
