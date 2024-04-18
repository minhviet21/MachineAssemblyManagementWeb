from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ProductComponent, Component, Order, ProductInOrder, ComponentQuantity, Product
from django.urls import reverse

def homepage(request):
    return render(request, "myproject/homepage.html")

def manager(request):
    return render(request, "myproject/manager.html")

def staff(request):
    return render(request, "myproject/staff.html")

class Product_:
    def main(request):
        list_product = Product.objects.all()
        context = {"list_product": list_product}
        return render(request, "myproject/product/main.html", context)

    def add_product(request):
        if request.method == "POST":
            product_type = request.POST.get('product_type')
            if not (Product.objects.filter(product_type=product_type).exists()):
                product = Product(product_type=product_type)
                product.save()
            return redirect('manager/product')
        return render(request, "myproject/product/add_product.html")

    def show_component(request, product_type):
        product = get_object_or_404(Product, product_type=product_type)
        list_pro_com = ProductComponent.objects.filter(product_type=product.product_type)
        context = {"list_pro_com": list_pro_com, "product": product}
        return render(request, "myproject/product/show_component.html", context)

    def add_component(request, product_type):
        product = get_object_or_404(Product, product_type=product_type)
        if request.method == 'POST':
            component_type = request.POST.get('component_type')
            quantity = request.POST.get('quantity')
            if int(quantity) > 0 \
                and (not ProductComponent.objects.filter(product_type=product.product_type, component_type=component_type).exists()):
                pro_com = ProductComponent(product_type=product.product_type, component_type=component_type, quantity=quantity)
                pro_com.save()
            return redirect(reverse('manager/product/product_type', kwargs={'product_type': product_type}))
        else:
            pro_com = None
        return render(request, "myproject/product/add_component.html", {'pro_com': pro_com, 'product': product})

    def update_component(request, product_type, component_type):
        pro_com = get_object_or_404(ProductComponent, product_type=product_type, component_type=component_type)
        if request.method == 'POST':
            quantity = request.POST.get('quantity')
            if int(quantity) <= 0:
                pro_com.delete()
            else:
                pro_com.quantity = quantity
                pro_com.save()
            return redirect(reverse('manager/product/product_type', kwargs={'product_type': product_type}))
        return render(request, "myproject/product/update_component.html", {'pro_com': pro_com})

class Component_:
    def main(request):
        list_component = Component.objects.all()
        context = {"list_component": list_component}
        return render(request, "myproject/component/main.html", context)

    def update(request, component_type):
        component = get_object_or_404(Component, component_type=component_type)
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

class Order_:
    def main(request):
        list_order = Order.objects.all()
        context = {"list_order": list_order}
        return render(request, "myproject/order/main.html", context)