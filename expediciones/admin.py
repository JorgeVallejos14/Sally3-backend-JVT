from django.contrib import admin
from .models import Region, Participante, Expedicion, Informe

# Register your models here.
admin.site.site_header = "Administracion de Expediciones"
admin.site.site_title = "Expediciones"
admin.site.index_title = "Gestion de la Resistencia"


class InformeInline(admin.StackedInline):
    model = Informe
    extra = 0


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'clima', 'nivel_peligro', 'total_expediciones')
    search_fields = ('nombre',)

    @admin.display(description='Expediciones')
    def total_expediciones(self, obj):
        return obj.expediciones.count()


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'especialidad')
    list_filter = ('especie',)
    search_fields = ('nombre', 'especialidad')


@admin.register(Expedicion)
class ExpedicionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'region', 'estado', 'fecha_inicio',
                    'duracion_dias', 'total_participantes')
    list_filter = ('estado', 'region')
    search_fields = ('titulo', 'objetivo')
    date_hierarchy = 'fecha_inicio'
    list_select_related = ('region',)
    filter_horizontal = ('participantes',)
    inlines = [InformeInline]
    actions = ['marcar_completada']

    fieldsets = (
        ('Datos generales', {
            'fields': ('titulo', 'region', 'estado')
        }),
        ('Calendario', {
            'fields': (('fecha_inicio', 'duracion_dias'),)
        }),
        ('Equipo y objetivo', {
            'fields': ('participantes', 'objetivo')
        }),
    )

    @admin.display(description='Participantes')
    def total_participantes(self, obj):
        return obj.participantes.count()

    @admin.action(description="Marcar como completadas")
    def marcar_completada(self, request, queryset):
        n = queryset.update(estado='ok')
        self.message_user(request, f"{n} expediciones marcadas como completadas")