from django.db import models

# Create your models here.
class Region(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    clima = models.CharField(max_length=60)
    nivel_peligro = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Participante(models.Model):
    nombre = models.CharField(max_length=80)
    especie = models.CharField(max_length=60)
    especialidad = models.CharField(max_length=80)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Expedicion(models.Model):
    ESTADOS = [
        ('plan', 'Planificada'),
        ('curso', 'En curso'),
        ('ok', 'Completada'),
        ('fallida', 'Fallida'),
    ]

    titulo = models.CharField(max_length=120)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='expediciones',
    )
    participantes = models.ManyToManyField(
        Participante,
        related_name='expediciones',
        blank=True,
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default='plan')
    fecha_inicio = models.DateField()
    duracion_dias = models.PositiveSmallIntegerField(default=1)
    objetivo = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name_plural = 'expediciones'

    def __str__(self):
        return self.titulo


class Informe(models.Model):
    expedicion = models.OneToOneField(
        Expedicion,
        on_delete=models.CASCADE,
        related_name='informe',
    )
    resultado = models.TextField()
    anillos_recuperados = models.PositiveIntegerField(default=0)
    heridos = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"Informe de {self.expedicion}"