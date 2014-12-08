from django.shortcuts import render
from .models import POI

def poi_list(request):
    pois = POI.objects.all()
    pois_bound = POI.objects.bound()
    
    return render(request, 'poi_list.html', {'pois': pois, 'pois_bound': pois_bound})
