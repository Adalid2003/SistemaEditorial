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
    path('registro/', views.registro, name='registro'),
    path('soli_estimacion/', views.soli_estimacion, name='soli_estimacion'),
    path('nueva_obra/', views.nueva_obra, name='nueva_obra'),
    path('estimaciones_cliente/', views.estimaciones_cliente, name='estimaciones_cliente'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)