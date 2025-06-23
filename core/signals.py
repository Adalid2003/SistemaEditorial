from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Material, CostoEstimacion

@receiver(post_save, sender=Material)
def actualizar_estimaciones(sender, instance, **kwargs):
    """
    Recalcula las estimaciones asociadas con las obras que utilizan el material modificado.
    """
    # Obtener todas las obras que utilizan el material modificado
    obras = instance.obra_set.all()  # Relación inversa desde Obra hacia Material

    for obra in obras:
        # Obtener las estimaciones asociadas a la obra
        estimaciones = CostoEstimacion.objects.filter(id_obra=obra)
        for estimacion in estimaciones:
            estimacion.calcular_estimacion()  # Recalcular el costo total
            estimacion.save()  # Guardar los cambios