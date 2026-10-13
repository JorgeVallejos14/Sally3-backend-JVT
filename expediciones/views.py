from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from .models import Expedicion, Region, Participante, Informe

# Create your views here.
def inicio(request):
    region_id = request.GET.get('region', '')
    estado = request.GET.get('estado', '')

    base = Expedicion.objects.all()
    if region_id.isdigit():
        base = base.filter(region_id=int(region_id))
    if estado:
        base = base.filter(estado=estado)

    total_anillos = Informe.objects.filter(expedicion__in=base).aggregate(
        total=Sum('anillos_recuperados')
    )['total'] or 0

    expediciones = base.select_related('region').annotate(
        num_participantes=Count('participantes')
    )

    contexto = {
        'expediciones': expediciones,
        'regiones': Region.objects.all(),
        'estados': Expedicion.ESTADOS,
        'region_sel': region_id,
        'estado_sel': estado,
        'total_anillos': total_anillos,
    }
    return render(request, 'expediciones/inicio.html', contexto)


def detalle(request, id):
    expedicion = get_object_or_404(
        Expedicion.objects.select_related('region').prefetch_related('participantes'),
        id=id,
    )
    return render(request, 'expediciones/detalle.html', {'expedicion': expedicion})


def participantes(request):
    lista = Participante.objects.annotate(
        num_expediciones=Count('expediciones')
    ).order_by('-num_expediciones', 'nombre')
    return render(request, 'expediciones/participantes.html', {'participantes': lista})