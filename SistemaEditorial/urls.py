"""
URL configuration for SistemaEditorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('login_empleado/', views.login_empleado, name='login_empleado'),
    path('registro/', views.registro, name='registro'),
    path('estimaciones_cliente/', views.estimaciones_cliente, name='estimaciones_cliente'),
    path('materiales/', views.materiales, name='materiales'),
    path('materiales/agregar/', views.agregar_material, name='agregar_material'),
    path('materiales/editar/<int:id_material>/', views.editar_material, name='editar_material'),
    path('materiales/eliminar/<int:id_material>/', views.eliminar_material, name='eliminar_material'),
    path('logout/', views.logout, name='logout'),
    path('obras/', views.obras, name='obras'),
    path('obras/agregar/', views.agregar_obra, name='agregar_obra'),
    path('obras/editar/<int:id_obra>/', views.editar_obra, name='editar_obra'),
    path('obras/eliminar/<int:id_obra>/', views.eliminar_obra, name='eliminar_obra'),
    path('registro_empleado/', views.registro_empleado, name='registro_empleado'),
    path('maquinaria/', views.maquinaria, name='maquinaria'),
    path('maquinaria/agregar/', views.agregar_maquinaria, name='agregar_maquinaria'),
    path('maquinaria/editar/<int:id_maquinaria>/', views.editar_maquinaria, name='editar_maquinaria'),
    path('maquinaria/eliminar/<int:id_maquinaria>/', views.eliminar_maquinaria, name='eliminar_maquinaria'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
