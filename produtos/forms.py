# produtos/forms.py
from django import forms
from .models import Variacao
from django.forms.models import BaseInlineFormSet

class VariacaoObrigatoria(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(VariacaoObrigatoria, self)._construct_form(i, **kwargs)
        form.empty_permitted = False  # Torna os campos obrigatórios
        return form
