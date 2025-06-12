from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
import os
from decimal import Decimal
from core.models import Cliente, Empleado, CostoEstimacion, Material, TipoMaterial, Maquinaria, TipoMaquinaria, Obra, Estado

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
                return redirect('obras')  # Redirigir a estimaciones del cliente
        except Cliente.DoesNotExist:
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


def registro_empleado(request):
    if request.method == 'POST':
        nombre = request.POST['username']
        correo = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validar el formato del correo electrónico
        try:
            validate_email(correo)
        except ValidationError:
            return render(request, 'registro_empleado.html', {'error': 'El formato del correo electrónico es inválido'})

        # Validar que las contraseñas coincidan
        if password1 != password2:
            return render(request, 'registro_empleado.html', {'error': 'Las contraseñas no coinciden'})

        # Validar que el correo no esté registrado
        if Empleado.objects.filter(correo=correo).exists():
            return render(request, 'registro_empleado.html', {'error': 'El correo ya está registrado'})

        # Crear el nuevo empleado
        Empleado.objects.create(
            nombreEmpleado=nombre,
            correo=correo,
            clave=make_password(password1)
        )

        # Enviar indicador de éxito
        return render(request, 'registro_empleado.html', {'success': 'El registro fue exitoso'})

    return render(request, 'registro_empleado.html')

def login_empleado(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        password = request.POST['password']

        # Intentar autenticar como empleado
        try:
            empleado = Empleado.objects.get(nombreEmpleado=nombre)
            if check_password(password, empleado.clave):
                # Guardar sesión del empleado
                request.session['usuario_tipo'] = 'empleado'
                request.session['usuario_id'] = empleado.id_empleado
                return redirect('materiales')  # Redirigir a la lista de materiales
        except Empleado.DoesNotExist:
            pass

        # Si no se encuentra el empleado
        return render(request, 'login_empleado.html', {'error': 'Nombre o contraseña incorrectos'})

    return render(request, 'login_empleado.html')

def estimaciones_cliente(request):
    if request.session.get('usuario_tipo') == 'cliente':  # Verificar si el usuario es cliente
        cliente_id = request.session.get('usuario_id')
        cliente = Cliente.objects.get(id_cliente=cliente_id)
        estimaciones = CostoEstimacion.objects.filter(id_obra__id_cliente=cliente)  # Filtrar estimaciones del cliente

        return render(request, 'estimaciones_cliente.html', {
            'estimaciones': estimaciones,
            'usuario_tipo': 'cliente'  # Pasar el estado de la sesión al contexto
        })
    else:
        return redirect('login')  # Redirigir al login si no está autenticado como cliente
# CRUD de Materiales
# Vista para mostrar la lista de materiales y tipos de material

def materiales(request):
    if request.session.get('usuario_tipo') == 'empleado':  # Verificar si el usuario es un empleado
        materiales = Material.objects.all()
        tipos_material = TipoMaterial.objects.all()
        return render(request, 'materiales.html', {
            'materiales': materiales,
            'tipos_material': tipos_material,
            'usuario_tipo': 'empleado'  # Pasar el estado de la sesión al contexto
        })
    else:
        return render(request, 'login_empleado.html', {
            'error': 'Debes iniciar sesión como empleado para acceder a esta página.'
        })

# Vista para agregar un nuevo material

def agregar_material(request):
    if request.method == 'POST':
        tipo_id = request.POST.get('id_tipoMaterial')  # Usa el nombre correcto del campo
        print("ID Tipo Material recibido:", tipo_id)  # Depuración
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        costo_unitario = request.POST.get('costo_unitario')
        unidad_medida = request.POST.get('unidad_medida')
        try:
            tipo = TipoMaterial.objects.get(id_tipoMaterial=tipo_id)  # Usa el nombre correcto del campo
            Material.objects.create(
                id_tipoMaterial=tipo,
                nombreMaterial=nombre,
                descripcion=descripcion,
                costoUnitarioMaterial=costo_unitario,
                unidadMedidaMaterial=unidad_medida
            )
        except TipoMaterial.DoesNotExist:
            print("El TipoMaterial con ID", tipo_id, "no existe.")  # Depuración
            return redirect('materiales')  # O muestra un mensaje de error
    return redirect('materiales')

# Vista para editar un material existente

def editar_material(request, id_material):
    material = Material.objects.get(id_material=id_material)
    if request.method == 'POST':
        tipo_id = request.POST.get('id_tipomaterial')
        material.id_tipomaterial = TipoMaterial.objects.get(id_tipomaterial=tipo_id)
        material.nombre = request.POST.get('nombre')
        material.descripcion = request.POST.get('descripcion')
        material.costo_unitario = request.POST.get('costo_unitario')
        material.unidad_medida = request.POST.get('unidad_medida')
        material.save()
        return redirect('materiales')
    # Si quieres permitir edición por GET, puedes retornar el modal aquí
    return redirect('materiales')

# Vista para eliminar un material

def eliminar_material(request, id_material):
    if request.method == 'POST':
        material = Material.objects.get(id_material=id_material)
        material.delete()
    return redirect('materiales')

def agregar_tipo_material(request):
    if request.session.get('usuario_tipo') == 'empleado':  # Verificar si el usuario es un empleado
        if request.method == 'POST':
            tipo_material = request.POST.get('tipoMaterial')  # Asegúrate de que el nombre coincida con el campo del modelo
            TipoMaterial.objects.create(tipoMaterial=tipo_material)  # Usa el nombre correcto del campo
        return redirect('materiales')
    else:
        return render(request, 'login_empleado.html', {
            'error': 'Debes iniciar sesión como empleado para acceder a esta página.'
        })

def obras(request):
    if request.session.get('usuario_tipo') == 'cliente':
        cliente_id = request.session.get('usuario_id')
        cliente = Cliente.objects.get(id_cliente=cliente_id)
        obras = Obra.objects.filter(id_cliente=cliente)  # Filtrar obras del cliente autenticado
        materiales = Material.objects.all()  # Obtener todos los materiales
        maquinarias = Maquinaria.objects.all()  # Obtener todas las maquinarias
        return render(request, 'obras.html', {
            'obras': obras,
            'materiales': materiales,
            'maquinarias': maquinarias,
            'usuario_tipo': 'cliente'
        })
    else:
        return redirect('login')  # Redirigir al login si no está autenticado como cliente


def agregar_obra(request):
    if request.method == 'POST':
        titulo = request.POST.get('tituloObra')
        autor = request.POST.get('nombreAutorObra')
        propietario = request.POST.get('propietarioObra')
        paginas = request.POST.get('numeroPaginas')
        tirada = request.POST.get('tirada')
        portada = request.FILES.get('portada')
        material_id = request.POST.get('id_material')
        maquinaria_id = request.POST.get('id_maquinaria')

        # Validaciones
        if not titulo or not autor or not propietario or not paginas or not tirada or not material_id or not maquinaria_id:
            return render(request, 'obras.html', {
                'error': 'Todos los campos son obligatorios.',
                'obras': Obra.objects.all(),
                'materiales': Material.objects.all(),
                'maquinarias': Maquinaria.objects.all()
            })

        if int(paginas) <= 0 or int(tirada) <= 0:
            return render(request, 'obras.html', {
                'error': 'El número de páginas y la tirada deben ser valores positivos.',
                'obras': Obra.objects.all(),
                'materiales': Material.objects.all(),
                'maquinarias': Maquinaria.objects.all()
            })

        if portada:
            extension = os.path.splitext(portada.name)[1].lower()
            if extension not in ['.png', '.jpg', '.jpeg']:
                return render(request, 'obras.html', {
                    'error': 'El archivo de portada debe estar en formato PNG, JPG o JPEG.',
                    'obras': Obra.objects.all(),
                    'materiales': Material.objects.all(),
                    'maquinarias': Maquinaria.objects.all()
                })

        try:
            cliente = Cliente.objects.get(id_cliente=request.session.get('usuario_id'))
            material = Material.objects.get(id_material=material_id)
            maquinaria = Maquinaria.objects.get(id_maquinaria=maquinaria_id)
            estado_inicial = Estado.objects.get(nombreEstado='espera')
        except Cliente.DoesNotExist:
            return render(request, 'obras.html', {'error': 'Cliente no encontrado.'})
        except Material.DoesNotExist:
            return render(request, 'obras.html', {'error': 'Material no encontrado.'})
        except Maquinaria.DoesNotExist:
            return render(request, 'obras.html', {'error': 'Maquinaria no encontrada.'})
        except Estado.DoesNotExist:
            return render(request, 'obras.html', {'error': 'Estado inicial no encontrado.'})

        # Crear la obra
        Obra.objects.create(
            tituloObra=titulo,
            nombreAutorObra=autor,
            propietarioObra=propietario,
            numeroPaginas=paginas,
            tirada=tirada,
            portada=portada,
            id_cliente=cliente,
            id_material=material,
            id_maquinaria=maquinaria,
            id_estado=estado_inicial
        )
        return redirect('obras')
    return render(request, 'obras.html')


def editar_obra(request, id_obra):
    obra = Obra.objects.get(id_obra=id_obra)
    if request.method == 'POST':
        obra.tituloObra = request.POST.get('tituloObra')
        obra.nombreAutorObra = request.POST.get('nombreAutorObra')
        obra.propietarioObra = request.POST.get('propietarioObra')
        obra.numeroPaginas = request.POST.get('numeroPaginas')
        obra.tirada = request.POST.get('tirada')
        if 'portada' in request.FILES:
            obra.portada = request.FILES.get('portada')
        obra.id_material = Material.objects.get(id_material=request.POST.get('id_material'))
        obra.id_maquinaria = Maquinaria.objects.get(id_maquinaria=request.POST.get('id_maquinaria'))
        obra.id_estado = Estado.objects.get(id_estado=request.POST.get('id_estado'))  # Actualizar estado
        obra.save()
        return redirect('obras')
    materiales = Material.objects.all()
    maquinarias = Maquinaria.objects.all()
    estados = Estado.objects.all()  # Obtener todos los estados
    return render(request, 'editar_obra.html', {
        'obra': obra,
        'materiales': materiales,
        'maquinarias': maquinarias,
        'estados': estados
    })


def eliminar_obra(request, id_obra):
    obra = Obra.objects.get(id_obra=id_obra)
    obra.delete()
    return redirect('obras')

from django.shortcuts import render, redirect, get_object_or_404
from core.models import Obra, CostoEstimacion, Estado, Empleado

def estimar_obra(request, id_obra):
    if request.session.get('usuario_tipo') != 'empleado':  # Verificar si el usuario es empleado
        return redirect('login_empleado')

    obra = get_object_or_404(Obra, id_obra=id_obra)

    if request.method == 'POST':
        # Obtener los valores ingresados por el empleado
        depreciacion = Decimal(request.POST.get('depreciacionEquipo'))
        energia = Decimal(request.POST.get('energiaElectrica'))
        costo_produccion = Decimal(request.POST.get('costoProduccion'))

        # Validar que los valores sean positivos
        if depreciacion <= 0 or energia <= 0 or costo_produccion <= 0:
            return render(request, 'estimar_obra.html', {
                'obra': obra,
                'error': 'Los valores deben ser positivos.'
            })

        # Obtener el empleado actual
        empleado = Empleado.objects.get(id_empleado=request.session.get('usuario_id'))

        # Crear la estimación
        costo_estimacion = CostoEstimacion(
            id_obra=obra,
            id_empleado=empleado,
            depreciacionEquipo=depreciacion,
            energiaElectrica=energia,
            costoProduccion=costo_produccion
        )
        costo_estimacion.calcular_estimacion()
        costo_estimacion.save()

        # Cambiar el estado de la obra a "estimada"
        obra.id_estado = Estado.objects.get(nombreEstado='estimada')
        obra.save()

        return redirect('obras_empleado')

    return render(request, 'estimar_obra.html', {'obra': obra})
def obras_empleado(request):
    if request.session.get('usuario_tipo') != 'empleado':  # Verificar si el usuario es empleado
        return redirect('login_empleado')

    obras = Obra.objects.all()  # Mostrar todas las obras
    estados = Estado.objects.all()  # Obtener todos los estados
    return render(request, 'obras_empleado.html', {
        'obras': obras,
        'estados': estados,
        'usuario_tipo': 'empleado'
    })

def maquinaria(request):
    if request.session.get('usuario_tipo') == 'empleado':  # Verificar si el usuario es un empleado
        maquinarias = Maquinaria.objects.all()
        tipos_maquinaria = TipoMaquinaria.objects.all()
        return render(request, 'maquinaria.html', {
            'maquinarias': maquinarias,
            'tipos_maquinaria': tipos_maquinaria,
            'usuario_tipo': 'empleado'  # Pasar el estado de la sesión al contexto
        })
    else:
        return render(request, 'login_empleado.html', {
            'error': 'Debes iniciar sesión como empleado para acceder a esta página.'
        })

def agregar_maquinaria(request):
    if request.method == 'POST':
        tipo_id = request.POST.get('id_tipoMaquinaria')
        nombre = request.POST.get('nombreMaquinaria')
        vida_util = request.POST.get('vidaUtilAnion')
        consumo = request.POST.get('consumoEnergiaKw')
        tipo = TipoMaquinaria.objects.get(id_tipoMaquinaria=tipo_id)
        Maquinaria.objects.create(
            id_tipoMaquinaria=tipo,
            nombreMaquinaria=nombre,
            vidaUtilAnion=vida_util,
            consumoEnergiaKw=consumo
        )
    return redirect('maquinaria')

def agregar_tipo_maquinaria(request):
    if request.session.get('usuario_tipo') == 'empleado':  # Verificar si el usuario es un empleado
        if request.method == 'POST':
            tipo_maquinaria = request.POST.get('tipoMaquinaria')
            TipoMaquinaria.objects.create(tipoMaquinaria=tipo_maquinaria)
        return redirect('maquinaria')
    else:
        return render(request, 'login_empleado.html', {
            'error': 'Debes iniciar sesión como empleado para acceder a esta página.'
        })

def editar_maquinaria(request, id_maquinaria):
    maq = Maquinaria.objects.get(id_maquinaria=id_maquinaria)
    if request.method == 'POST':
        tipo_id = request.POST.get('id_tipoMaquinaria')
        maq.id_tipoMaquinaria = TipoMaquinaria.objects.get(id_tipoMaquinaria=tipo_id)
        maq.nombreMaquinaria = request.POST.get('nombreMaquinaria')
        maq.vidaUtilAnion = request.POST.get('vidaUtilAnion')
        maq.consumoEnergiaKw = request.POST.get('consumoEnergiaKw')
        maq.save()
        return redirect('maquinaria')
    return redirect('maquinaria')

def eliminar_maquinaria(request, id_maquinaria):
    if request.method == 'POST':
        maq = Maquinaria.objects.get(id_maquinaria=id_maquinaria)
        maq.delete()
    return redirect('maquinaria')

def logout(request):
    # Eliminar la sesión del usuario
    request.session.flush()
    return redirect('login')  # Redirigir al login después de cerrar sesión