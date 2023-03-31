from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    data_nasc = models.DateField('data nascimento', null=True)
    cpf = models.CharField(max_length=11, unique=True, validators=[
        RegexValidator(r'^\d{11}$', 'O CPF deve ter 11 dígitos')
    ])
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)
    foto_perfil = models.ImageField(upload_to='foto_perfil/', blank=True, null=True)

    def clean(self):
        # Validar CPF
        cpf = self.cpf
        if not self.pk:  # novo objeto, valida CPF
            cpf_valido = self.validar_cpf(cpf)
            if not cpf_valido:
                raise ValidationError('CPF inválido.')
        else:  # objeto existente, mantém CPF
            obj = Pessoa.objects.get(pk=self.pk)
            if obj.cpf != cpf:
                raise ValidationError('CPF não pode ser alterado.')

    @staticmethod
    def validar_cpf(cpf):

        cpf = cpf.replace('.', '').replace('-', '')  # remove pontos e hífen
        if not cpf.isdigit() or len(cpf) != 11:  # verifica se é numérico e tem 11 dígitos
            return False

        ''' calcula os dígitos verificadores '''
        soma = sum([int(cpf[i]) * (10-i) for i in range(9)])
        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto

        soma = sum([int(cpf[i]) * (11-i) for i in range(10)])
        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto

        '''verifica se os dígitos verificadores são iguais aos informado'''
        if cpf[-2:] == f'{digito1}{digito2}':
            return True
        else:
            return False
