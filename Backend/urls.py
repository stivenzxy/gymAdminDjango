"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gym.views import CreateReservaView, GetReservasView, PenalizarView, ReservasPorUsuarioView
from gym.views import LoginView, CheckUserView, CreateUserView, ReporteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('CheckUser/', CheckUserView.as_view(), name='Check User'),
    path('CreateUser/', CreateUserView.as_view(), name='Create User'),
    path('Reporte/', ReporteView.as_view(), name='Reporte'),
    path('Reporte/', ReporteView.as_view(), name='Reporte'),
    path('CreateReserva/', CreateReservaView.as_view(), name='Crear Reserva'),
    path('ReservasPerUser/', ReservasPorUsuarioView.as_view(), name='Reservas por Usuario'),
    path('GetReservas/', GetReservasView.as_view(), name='Reservas'),
    path('Penalizar/', PenalizarView.as_view(), name='Penalizar')
]

