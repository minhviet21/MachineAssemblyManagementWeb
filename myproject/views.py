from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ProductComponent

def homepage(request):
    return render(request, "myproject/homepage.html")

def index(request):
    list_product = ProductComponent.objects.all()
    context = {"list_product": list_product}
    return render(request, "myproject/index.html", context)

def productcomponent(request):
    list_pro_com = ProductComponent.objects.all()
    context = {"list_pro_com": list_pro_com}
    return render(request, "myproject/productcomponent.html", context)

def updateproductcomponent(request, id):
    pro_com = get_object_or_404(ProductComponent, id=id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        pro_com.quantity = quantity
        pro_com.save()
        return redirect('productcomponent')
    return render(request, "myproject/updateproductcomponent.html", {'pro_com': pro_com})

def update(request, id):
    aa = get_object_or_404(AA, id=id)
    if request.method == 'POST':
        x = request.POST.get('x')
        y = request.POST.get('y')
        # Update the attributes of aa
        aa.x = x
        aa.y = y
        aa.save()
        return redirect('AA')  # replace 'success_url' with your desired redirect URL
    return render(request, "myproject/update.html", {'aa': aa})