from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from core.models import Cliente, Empleado, CostoEstimacion, Material, Maquinaria, TipoMaquinaria

def login(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']

        # Validar el formato del correo electrónico
        try:
            validate_email(correo)
        except ValidationError:
            return render(request, 'login.html', {'error': 'El formato del correo electrónico es inválido'})

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
    # Filtrar estimaciones según el cliente autenticado
    cliente = request.user.cliente  # Suponiendo que el cliente está autenticado
    estimaciones = CostoEstimacion.objects.filter(id_obra__id_cliente=cliente)

    return render(request, 'estimaciones_cliente.html', {'estimaciones': estimaciones})