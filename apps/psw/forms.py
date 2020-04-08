from django import forms


class FormPswLogin(forms.Form):
    """
        Este é o formulário onde o usuário informa seu login e senha de acesso do sistema PSW da Copel.
    """

    username = forms.CharField(max_length=150, label='Chave Copel')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha Copel')

    widgets = {
        'password': forms.PasswordInput(),
    }


class FormPswContrato(forms.Form):
    """
        Este é o formulário onde o usuário informa o contrato que deseja buscar no sistema da Copel. Posteriormente este
    sistema envia as informações deste contrato para o sistema principal (Constel.tk) para serem armazedas e realizar a
    gestão da ONT utilizada.
    """

    contrato = forms.CharField(min_length=5, max_length=7)
