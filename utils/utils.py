import json
from django.utils.safestring import SafeString


def formata_preco(val):
    try:
        # Tenta converter o valor para float antes de formatá-lo
        val = float(val)
        return f'R$ {val:.2f}'.replace('.', ',')
    except (ValueError, TypeError):
        # Se não for um número válido, retorna um valor padrão
        return 'R$ 0,00'

def cart_total_qtd(carrinho):
    # Se for SafeString ou string, converte para dicionário
    if isinstance(carrinho, SafeString) or isinstance(carrinho, str):
        try:
            carrinho = json.loads(carrinho)  # Converte JSON para dicionário
        except json.JSONDecodeError:
            return 0  # Se falhar, assume que o carrinho está vazio

    # Garante que é um dicionário antes de acessar .values()
    if isinstance(carrinho, dict):
        return sum([item['quantidade'] for item in carrinho.values()])

    return 0  # Se não for dicionário, retorna 0

def cart_totals(carrinho):
    # Se for SafeString ou string, converte para dicionário
    if isinstance(carrinho, SafeString) or isinstance(carrinho, str):
        try:
            carrinho = json.loads(carrinho)  # Converte JSON para dicionário
        except json.JSONDecodeError:
            return 0  # Se falhar, assume que o carrinho está vazio

    # Garante que é um dicionário antes de acessar .values()
    if isinstance(carrinho, dict):
        return sum(
            [
                item.get('preco_quantitativo_promocional')
                if item.get('preco_quantitativo_promocional')
                else item.get('preco_quantitativo')
                for item in carrinho.values()
            ]
        )

    return 0  # Se não for dicionário, retorna 0
