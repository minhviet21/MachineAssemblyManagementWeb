from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ProductComponent, Component, Order, ProductInOrder, ComponentQuantity, Product

def homepage(request):
    return render(request, "myproject/homepage.html")

def manager(request):
    return render(request, "myproject/manager.html")

def staff(request):
    return render(request, "myproject/staff.html")

class Product_Component:
    def main(request):
        list_pro_com = ProductComponent.objects.all()
        context = {"list_pro_com": list_pro_com}
        return render(request, "myproject/productcomponent/main.html", context)

    def update(request, id):
        pro_com = get_object_or_404(ProductComponent, id=id)
        if request.method == 'POST':
            quantity = request.POST.get('quantity')
            if int(quantity) <= 0:
                pro_com.delete()
            else:
                pro_com.quantity = quantity
                pro_com.save()
            return redirect('manager/productcomponent')
        return render(request, "myproject/productcomponent/update.html", {'pro_com': pro_com})

    def add(request):
        if request.method == 'POST':
            product_type = request.POST.get('product_type')
            component_type = request.POST.get('component_type')
            #check if component_type is in Component
            if not Component.objects.filter(component_type=component_type).exists():
                return redirect('manager/productcomponent')
            quantity = request.POST.get('quantity')
            if int(quantity) > 0:
                pro_com = ProductComponent(product_type=product_type, component_type=component_type, quantity=quantity)
                pro_com.save()
            return redirect('manager/productcomponent')
        else:
            pro_com = None
        return render(request, "myproject/productcomponent/add.html", {'pro_com': pro_com})

class Component_:
    def main(request):
        list_component = Component.objects.all()
        context = {"list_component": list_component}
        return render(request, "myproject/component/main.html", context)

    def update(request, id):
        component = get_object_or_404(Component, id=id)
        if request.method == 'POST':
            supplier_name = request.POST.get('supplier_name')
            supplier_address = request.POST.get('supplier_address')
            if supplier_name == '' or supplier_address == '':
                component.delete()
            else:
                component.supplier_name = supplier_name
                component.supplier_address = supplier_address
                component.save()
            return redirect('manager/component')
        return render(request, "myproject/component/update.html", {'component': component})

    def add(request):
        if request.method == 'POST':
            component_type = request.POST.get('component_type')
            supplier_name = request.POST.get('supplier_name')
            supplier_address = request.POST.get('supplier_address')
            component = Component(component_type=component_type, supplier_name=supplier_name, supplier_address=supplier_address)
            component.save()
            return redirect('manager/component')
        else:
            component = None
        return render(request, "myproject/component/add.html", {'component': component})