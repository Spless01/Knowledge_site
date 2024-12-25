from django import forms
from .models import KnowledgeField

class SearchForm(forms.Form):
    field = forms.ModelChoiceField(queryset=KnowledgeField.objects.all(), required=False, label='Галузь знань')
    query = forms.CharField(max_length=255, required=False, label='Пошук статей')
