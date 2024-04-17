from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ProductComponent

def homepage(request):
    return render(request, "myproject/homepage.html")

def manager(request):
    return render(request, "myproject/manager.html")

def staff(request):
    return render(request, "myproject/staff.html")

def productcomponent(request):
    list_pro_com = ProductComponent.objects.all()
    context = {"list_pro_com": list_pro_com}
    return render(request, "myproject/productcomponent.html", context)

def updateproductcomponent(request, id):
    pro_com = get_object_or_404(ProductComponent, id=id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if int(quantity) <= 0:
            pro_com.delete()
        else:
            pro_com.quantity = quantity
            pro_com.save()
        return redirect('manager/productcomponent')
    return render(request, "myproject/updateproductcomponent.html", {'pro_com': pro_com})

def addproductcomponent(request):
    if request.method == 'POST':
        product_type = request.POST.get('product_type')
        component_type = request.POST.get('component_type')
        quantity = request.POST.get('quantity')
        if int(quantity) > 0:
            pro_com = ProductComponent(product_type=product_type, component_type=component_type, quantity=quantity)
            pro_com.save()
        return redirect('manager/productcomponent')
    else:
        pro_com = None
    return render(request, "myproject/addproductcomponent.html", {'pro_com': pro_com})