from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Sala, Reserva
import datetime

class RegistrarUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Obrigatório. Informe um email válido."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este email já está cadastrado.")
        return email

class SalaForm(forms.ModelForm):
    capacidade = forms.IntegerField(min_value=1, help_text="Capacidade mínima: 1 pessoa")

    class Meta:
        model = Sala
        fields = ['nome', 'capacidade', 'descricao']
        help_texts = {
            'nome': "Nome único para identificação da sala",
            'descricao': "Informações adicionais sobre a sala (opcional)"
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if Sala.objects.filter(nome__iexact=nome).exists():
            raise ValidationError("Já existe uma sala com este nome.")
        return nome

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['sala', 'data', 'horario', 'descricao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().isoformat()}),
            'horario': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'descricao': "Informe o propósito da reserva (opcional)"
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['sala'].queryset = Sala.objects.filter(disponivel=True)
        
        # Definir o mínimo da data diretamente no widget
        self.fields['data'].widget.attrs['min'] = datetime.date.today().isoformat()

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        sala = cleaned_data.get('sala')
        horario = cleaned_data.get('horario')

        # Validação de data
        if data and data < datetime.date.today():
            self.add_error('data', "Não é possível reservar para datas passadas.")

        # Validação de conflito de reserva
        if all([data, sala, horario]):
            if Reserva.objects.filter(sala=sala, data=data, horario=horario).exists():
                self.add_error('horario', "Este horário já está reservado para esta sala.")

        return cleaned_data

    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data < datetime.date.today():
            raise ValidationError("A data da reserva não pode ser no passado.")
        return data