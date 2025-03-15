from django.contrib import admin
from .models import Produto, Variacao
from .forms import VariacaoObrigatoria

# Definir a classe VariacaoInline primeiro
class VariacaoInline(admin.TabularInline):
    model = Variacao
    formset = VariacaoObrigatoria
    min_num = 1  # Garante que pelo menos uma variação seja cadastrada
    extra = 0
    can_delete = True

# Depois, definir o ProdutoAdmin
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'get_preco_formatado', 'get_preco_promocional_formatado']
    inlines = [VariacaoInline]  # Aqui agora já está definido corretamente

# Registrar os modelos no Django Admin
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)

