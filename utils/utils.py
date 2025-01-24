def formata_preco(val):
    try:
        # Tenta converter o valor para float antes de formatá-lo
        val = float(val)
        return f'R$ {val:.2f}'.replace('.', ',')
    except (ValueError, TypeError):
        # Se não for um número válido, retorna um valor padrão
        return 'R$ 0,00'

def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def cart_totals(carrinho):
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item
            in carrinho.values()
        ]
    )
