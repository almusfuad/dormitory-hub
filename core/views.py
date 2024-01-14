from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
def home(request):
      return render(request, 'home.html')

class HomeView(ListView):
      template_name = 'home.html'