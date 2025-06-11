from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from core.models import Cliente, Empleado, CostoEstimacion, Material, Maquinaria, TipoMaquinaria

def login(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']

        try:
            cliente = Cliente.objects.get(correoElectronico=correo)
            if check_password(password, cliente.contraseña):
                request.session['usuario_tipo'] = 'cliente'
                request.session['usuario_id'] = cliente.id_cliente
                print("Cliente autenticado correctamente")  # Mensaje de depuración
                return redirect('estimaciones_cliente')
        except Cliente.DoesNotExist:
            pass

        try:
            empleado = Empleado.objects.get(correo=correo)
            if check_password(password, empleado.clave):
                request.session['usuario_tipo'] = 'empleado'
                request.session['usuario_id'] = empleado.id_empleado
                print("Empleado autenticado correctamente")  # Mensaje de depuración
                return redirect('admin/')
        except Empleado.DoesNotExist:
            pass

        print("Autenticación fallida")  # Mensaje de depuración
        return render(request, 'login.html', {'error': 'Correo o contraseña incorrectos'})

    return render(request, 'login.html', {'usuario_tipo': None})  # Pasar estado de sesión vacío

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validar el formato del correo electrónico
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'registro.html', {'error': 'El formato del correo electrónico es inválido'})

        # Validar que las contraseñas coincidan
        if password1 != password2:
            return render(request, 'registro.html', {'error': 'Las contraseñas no coinciden'})

        # Validar que el correo no esté registrado
        if Cliente.objects.filter(correoElectronico=email).exists():
            return render(request, 'registro.html', {'error': 'El correo ya está registrado'})

        # Crear el nuevo usuario
        Cliente.objects.create(
            nombreCliente=username,
            correoElectronico=email,
            contraseña=make_password(password1)
        )

        # Enviar indicador de éxito
        return render(request, 'registro.html', {'success': 'El registro fue exitoso'})

    return render(request, 'registro.html')

def soli_estimacion(request):
    return render(request, 'soli_estimacion.html', {})

def nueva_obra(request):
    return render(request, 'nueva_obra.html', {})


def estimaciones_cliente(request):
    if request.session.get('usuario_tipo') == 'cliente':
        cliente_id = request.session.get('usuario_id')
        cliente = Cliente.objects.get(id_cliente=cliente_id)
        estimaciones = CostoEstimacion.objects.filter(id_obra__id_cliente=cliente)
        return render(request, 'estimaciones_cliente.html', {
            'estimaciones': estimaciones,
            'usuario_tipo': 'cliente'  # Pasar el estado de la sesión
        })
    else:
        return redirect('login')  # Redirigir al login si no está autenticado como cliente

def logout(request):
    request.session.flush()  # Eliminar todos los datos de la sesión
    return redirect('login')  # Redirigir al login después de cerrar sesión