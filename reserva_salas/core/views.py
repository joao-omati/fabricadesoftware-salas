from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Sala, Reserva
from .forms import RegistrarUsuarioForm, SalaForm, ReservaForm
import datetime

class HomeView(View): # em python classes não usam anotação de tipo de retorno exemplo: class HomeView(View) -> HttResponse, somente funciona em funções e métodos
    def get(self, request:HttpRequest)->HttpResponse:
        salas = Sala.objects.filter(disponivel=True)[:5]
        hoje = datetime.date.today()
        reservas_hoje = Reserva.objects.filter(data=hoje).order_by('horario')[:5]
        return render(request, 'core/home.html', {
            'salas': salas,
            'reservas_hoje': reservas_hoje
        })

class RegistrarUsuarioView(View):
    def get(self, request:HttpRequest)->HttpResponse:
        form = RegistrarUsuarioForm()
        return render(request, 'core/registrar.html', {'form': form})
    
    def post(self, request:HttpRequest)->HttpResponse:
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('home')
        return render(request, 'core/registrar.html', {'form': form})

class LoginUsuarioView(View):
    def get(self, request:HttpRequest)->HttpResponse:
        return render(request, 'core/login.html')
    
    def post(self, request:HttpRequest)->HttpResponse:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Usuário ou senha incorretos.')
        return render(request, 'core/login.html')

class LogoutUsuarioView(LoginRequiredMixin, View):
    def get(self, request:HttpRequest)->HttpResponse:
        logout(request)
        return redirect('home')

class CriarSalaView(LoginRequiredMixin, CreateView):
    model = Sala
    form_class = SalaForm
    template_name = 'core/criar_sala.html'
    success_url = reverse_lazy('lista_salas')
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Sala criada com sucesso!')
        return super().form_valid(form)

class ListaSalasView(ListView):
    model = Sala
    template_name = 'core/lista_salas.html'
    context_object_name = 'salas'
    paginate_by = 10

class FazerReservaView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'core/fazer_reserva.html'
    success_url = reverse_lazy('minhas_reservas')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        sala_id = self.request.GET.get('sala')
        if sala_id:
            try:
                initial['sala'] = Sala.objects.get(id=sala_id)
            except Sala.DoesNotExist:
                pass
        return initial
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Reserva realizada com sucesso!')
        return super().form_valid(form)

class MinhasReservasView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'core/minhas_reservas.html'
    context_object_name = 'reservas'
    
    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user).order_by('-data', 'horario')

class CancelarReservaView(LoginRequiredMixin, DeleteView):
    model = Reserva
    template_name = 'core/cancelar_reserva.html'
    success_url = reverse_lazy('minhas_reservas')
    
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Reserva cancelada com sucesso!')
        return super().delete(request, *args, **kwargs)

class VerSalasView(View):
    def get(self, request:HttpRequest)->HttpResponse:
        salas = Sala.objects.filter(disponivel=True)
        hoje = datetime.date.today()
        amanha = hoje + datetime.timedelta(days=1)
        
        salas_info = []
        for sala in salas:
            reservas_hoje = Reserva.objects.filter(sala=sala, data=hoje).values_list('horario', flat=True)
            reservas_amanha = Reserva.objects.filter(sala=sala, data=amanha).values_list('horario', flat=True)
            
            salas_info.append({
                'sala': sala,
                'reservas_hoje': reservas_hoje,
                'reservas_amanha': reservas_amanha,
            })
        
        return render(request, 'core/ver_salas.html', {
            'salas_info': salas_info,
            'hoje': hoje,
            'amanha': amanha,
            'HORARIOS': Reserva.HORARIOS,
        })