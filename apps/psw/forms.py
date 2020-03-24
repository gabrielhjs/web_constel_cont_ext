from django import forms


class FormPswLogin(forms.Form):
    """
    Formulário de login de usuário
    """

    username = forms.CharField(max_length=150, label='Chave Copel')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha Copel')

    widgets = {
        'password': forms.PasswordInput(),
    }


class FormPswContrato(forms.Form):

    contrato = forms.CharField(min_length=5, max_length=7)
