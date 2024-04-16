from django.shortcuts import render
from django.http import HttpResponse
from .models import ProductComponent

def homepage(request):
    return render(request, "myproject/homepage.html")

def index(request):
    list_product = ProductComponent.objects.all()
    context = {"list_product": list_product}
    return render(request, "myproject/index.html", context)

def productcomponent(request):
    list_product = ProductComponent.objects.all()
    context = {"list_product": list_product}
    return render(request, "myproject/productcomponent.html", context)
