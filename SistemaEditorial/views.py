from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Cliente, Empleado

def login(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']

        # Intentar autenticar como cliente
        try:
            cliente = Cliente.objects.get(correoElectronico=correo)
            if check_password(password, cliente.contraseña):
                # Guardar sesión del cliente
                request.session['usuario_tipo'] = 'cliente'
                request.session['usuario_id'] = cliente.id_cliente
                return redirect('estimaciones_cliente')  # Redirigir a estimaciones del cliente
        except Cliente.DoesNotExist:
            pass

        # Intentar autenticar como empleado
        try:
            empleado = Empleado.objects.get(correo=correo)
            if check_password(password, empleado.clave):
                # Guardar sesión del empleado
                request.session['usuario_tipo'] = 'empleado'
                request.session['usuario_id'] = empleado.id_empleado
                return redirect('admin/')  # Redirigir al panel de administración
        except Empleado.DoesNotExist:
            pass

        # Si no se encuentra el usuario
        return render(request, 'login.html', {'error': 'Correo o contraseña incorrectos'})

    return render(request, 'login.html', {})

def registro(request):
    return render(request, 'registro.html', {})

def soli_estimacion(request):
    return render(request, 'soli_estimacion.html', {})

def nueva_obra(request):
    return render(request, 'nueva_obra.html', {})