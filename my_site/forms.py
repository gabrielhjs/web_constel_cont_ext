from django import forms


class FormLogin(forms.Form):
    """
    Formulário de login de usuário
    """

    username = forms.CharField(max_length=150, label='Matrícula')
    password = forms.CharField(widget=forms.PasswordInput)

    widgets = {
        'password': forms.PasswordInput(),
    }


class DateInput(forms.DateInput):
    input_type = 'date'


class FormDataInicialFinalFuncionario(forms.Form):
    """
    Formulário que permite selecionar uma data inicial e uma final
    """

    data_inicial = forms.DateField(widget=DateInput(), required=False)
    data_final = forms.DateField(widget=DateInput(), required=False)
    funcionario = forms.CharField(
        label='Funcionário',
        help_text='Insira alguma informação do funcionário',
        required=False
    )

    def clean(self):
        form_data = self.cleaned_data

        if form_data['data_inicial'] >= form_data['data_final']:
            self.errors['data_inicial'] = ['A data inicial não pode ser mais recente que a data final']

        return form_data


class FormDataInicialFinal(forms.Form):
    """
    Formulário que permite selecionar uma data inicial e uma final
    """

    data_inicial = forms.DateField(widget=DateInput(), required=False)
    data_final = forms.DateField(widget=DateInput(), required=False)

    def clean(self):
        form_data = self.cleaned_data

        if form_data['data_inicial'] >= form_data['data_final']:
            self.errors['data_inicial'] = ['A data inicial não pode ser mais recente que a data final']

        return form_data
