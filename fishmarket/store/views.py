from django.shortcuts import render
from .models import Fish

def home(request):
    fishes = Fish.objects.all()
    return render(request, 'home.html', {'fishes': fishes})
