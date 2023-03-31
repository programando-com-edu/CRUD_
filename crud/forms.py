from django import forms
from .models import Pessoa

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome', 'data_nasc', 'cpf', 'email', 'telefone', 'foto_perfil']

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if self.instance.pk:  # objeto existente, CPF já validado na model
            return cpf
        cpf_valido = Pessoa.validar_cpf(cpf)
        if not cpf_valido:
            raise forms.ValidationError('CPF inválido.')
        return cpf

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance.pk:  # objeto existente, e-mail já validado na model
            return email
        email_existe = Pessoa.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        if email_existe:
            raise forms.ValidationError('E-mail já existe.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('cpf')
        cpf_existe = Pessoa.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists()
        if cpf_existe:
            raise forms.ValidationError('CPF já existe.')
        return cleaned_data
