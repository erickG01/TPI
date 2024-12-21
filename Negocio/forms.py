from django import forms
from .models import ConfiguracionEmpresa

class ConfiguracionEmpresaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionEmpresa
        fields = ['nombre', 'slogan', 'logo']