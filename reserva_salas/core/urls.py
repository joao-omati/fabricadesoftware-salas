from django.urls import path
from .views import (
    HomeView, RegistrarUsuarioView, LoginUsuarioView, LogoutUsuarioView,
    CriarSalaView, ListaSalasView, FazerReservaView, MinhasReservasView,
    CancelarReservaView, VerSalasView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('registrar/', RegistrarUsuarioView.as_view(), name='registrar'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    
    path('salas/criar/', CriarSalaView.as_view(), name='criar_sala'),
    path('salas/', ListaSalasView.as_view(), name='lista_salas'),
    path('salas/disponibilidade/', VerSalasView.as_view(), name='ver_salas'),
    
    path('reservas/nova/', FazerReservaView.as_view(), name='fazer_reserva'),
    path('reservas/minhas/', MinhasReservasView.as_view(), name='minhas_reservas'),
    path('reservas/cancelar/<int:pk>/', CancelarReservaView.as_view(), name='cancelar_reserva'),
]