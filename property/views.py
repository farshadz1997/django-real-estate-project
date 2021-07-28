from django.shortcuts import render
from .models import Property
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.
def Home_Page(request):
    properties = Property.objects.all().order_by('-pub_date')[:6] # get last 6 items by publish date
    context = {
        "properties": properties,
    }
    return render(request, 'property/index.html', context)

class PropertiesList(ListView):
    model = Property
    template_name = 'property/properties-list.html'
    context_object_name = 'properties'
    ordering = ['-pub_date']
    paginate_by = 6