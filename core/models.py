from django.db import models

# Modelo para Cliente
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombreCliente = models.CharField(max_length=80)
    correoElectronico = models.EmailField(max_length=100, unique=True)
    contraseña = models.CharField(max_length=128)  # Usar hashing para seguridad

    def __str__(self):
        return self.nombreCliente


# Modelo para Empleado
class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombreEmpleado = models.CharField(max_length=80)
    correo = models.EmailField(max_length=100, unique=True)
    clave = models.CharField(max_length=128)  # Usar hashing para seguridad

    def __str__(self):
        return self.nombreEmpleado


# Modelo para Obra
class Obra(models.Model):
    id_obra = models.AutoField(primary_key=True)
    tituloObra = models.CharField(max_length=50)
    nombreAutorObra = models.CharField(max_length=50)
    propietarioObra = models.CharField(max_length=50)
    numeroPaginas = models.IntegerField()
    tirada = models.IntegerField()
    portada = models.ImageField(upload_to='portadas/')
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_material = models.ForeignKey('Material', on_delete=models.CASCADE)
    id_maquinaria = models.ForeignKey('Maquinaria', on_delete=models.CASCADE)

    def __str__(self):
        return self.tituloObra


# Modelo para Material
class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    nombreMaterial = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=500)
    costoUnitarioMaterial = models.DecimalField(max_digits=10, decimal_places=2)
    unidadMedidaMaterial = models.CharField(max_length=5)

    def __str__(self):
        return self.nombreMaterial


# Modelo para Maquinaria
class Maquinaria(models.Model):
    id_maquinaria = models.AutoField(primary_key=True)
    nombreMaquinaria = models.CharField(max_length=50)
    vidaUtilAnion = models.IntegerField()
    consumoEnergiaKw = models.DecimalField(max_digits=10, decimal_places=2)
    id_tipoMaquinaria = models.ForeignKey('TipoMaquinaria', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreMaquinaria


# Modelo para Tipo de Maquinaria
class TipoMaquinaria(models.Model):
    id_tipoMaquinaria = models.AutoField(primary_key=True)
    tipoMaquinaria = models.CharField(max_length=50)

    def __str__(self):
        return self.tipoMaquinaria


# Modelo para Tipo de Material
class TipoMaterial(models.Model):
    id_tipoMaterial = models.AutoField(primary_key=True)
    tipoMaterial = models.CharField(max_length=50)

    def __str__(self):
        return self.tipoMaterial


# Modelo para Costo de Estimación
class CostoEstimacion(models.Model):
    id_costoEstimacion = models.AutoField(primary_key=True)
    id_obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    depreciacionEquipo = models.DecimalField(max_digits=10, decimal_places=2)
    energiaElectrica = models.DecimalField(max_digits=10, decimal_places=2)
    costoProduccion = models.DecimalField(max_digits=10, decimal_places=2)
    tirada = models.IntegerField()
    totalEstimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calcular_estimacion(self):
        # Factores de estimación
        derechos_autor = self.id_obra.numeroPaginas * 0.05  # Ejemplo: 5% por página
        costos_administrativos = 1000  # Ejemplo: costo fijo
        costo_material = self.id_obra.id_material.costoUnitarioMaterial * self.tirada
        costo_maquinaria = self.id_obra.id_maquinaria.consumoEnergiaKw * self.energiaElectrica

        # Cálculo del costo total
        self.totalEstimado = (
            self.depreciacionEquipo +
            costo_material +
            costo_maquinaria +
            derechos_autor +
            costos_administrativos +
            self.costoProduccion
        )
        return self.totalEstimado

    def __str__(self):
        return f"Estimación {self.id_costoEstimacion} - Obra {self.id_obra}"
# Create your models here.
