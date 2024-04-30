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

    def add_order(request):
        if request.method == 'POST':
            if Order.objects.all().count() == 0:
                order_id = 1
            else:
                order_id = Order.objects.latest('order_id').order_id + 1
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            status = "Not produced"
            order = Order(order_id=order_id, address=address, phone_number=phone_number, status=status)
            order.save()
            return redirect('staff/order/order_id/show_product', order_id=order_id)
        return render(request, "myproject/order/add_order.html")

    def update_order(request, order_id):
        order = get_object_or_404(Order, order_id=order_id)
        if request.method == 'POST':
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            if address == '':
                ProductInOrder.objects.filter(order_id=order.order_id).delete()
                order.delete()
            else:
                order.address = address
                order.phone_number = phone_number
                order.save()
            return redirect('staff/order')
        return render(request, "myproject/order/update_order.html", {'order': order})

    def show_product(request, order_id):
        order = get_object_or_404(Order, order_id=order_id)
        list_pro_in_order = ProductInOrder.objects.filter(order_id=order.order_id)
        context = {"list_pro_in_order": list_pro_in_order, "order": order}
        return render(request, "myproject/order/show_product.html", context)

    def add_product(request, order_id):
        order = get_object_or_404(Order, order_id=order_id)
        if request.method == 'POST':
            product_type = request.POST.get('product_type')
            quantity = request.POST.get('quantity')
            if Product.objects.filter(product_type=product_type).exists() and int(quantity) > 0:
                pro_in_order = ProductInOrder(order_id=order.order_id, product_type=product_type, quantity=quantity)
                pro_in_order.save()
            return redirect(reverse('staff/order/order_id/show_product', kwargs={'order_id': order_id}))
        else:
            pro_in_order = None
        return render(request, "myproject/order/add_product.html", {'pro_in_order': pro_in_order, 'order': order})

    def update_product(request, order_id, product_type):
        pro_in_order = get_object_or_404(ProductInOrder, order_id=order_id, product_type=product_type)
        if request.method == 'POST':
            quantity = request.POST.get('quantity')
            if int(quantity) <= 0:
                pro_in_order.delete()
            else:
                pro_in_order.quantity = quantity
                pro_in_order.save()
            return redirect(reverse('staff/order/order_id/show_product', kwargs={'order_id': order_id}))
        return render(request, "myproject/order/update_product.html", {'pro_in_order': pro_in_order})

class Request_Production_:
    def main(request):
        ready_to_produce = Request_Production_.list_ordered_product()
        context = {"ready_to_produce": ready_to_produce}
        return render(request, "myproject/production/manager.html", context)

    def list_ordered_product():
        list_product = ProductInOrder.objects.filter(status="Not produced")
        ready_to_produce = []
        for product in list_product:
            if Request_Production_.check_ready(product):
                ready_to_produce.append(product)
        return ready_to_produce
        
    def check_ready(product_in_order):
        list_component = ProductComponent.objects.filter(product_type=product_in_order.product_type)
        for pro_com in list_component:
            component = get_object_or_404(ComponentQuantity, component_type=pro_com.component_type)
            if pro_com.quantity*product_in_order.quantity > component.now:
                return False
        return True
    
    def request_production(request, order_id, product_type):
        pro_in_order = get_object_or_404(ProductInOrder, order_id=order_id, product_type=product_type)
        if request.method == 'POST':
            list_component = ProductComponent.objects.filter(product_type=product_type)
            for pro_com in list_component:
                component = get_object_or_404(ComponentQuantity, component_type=pro_com.component_type)
                component.now -= pro_com.quantity*pro_in_order.quantity
                component.save()
            pro_in_order.status = "Producing"
            pro_in_order.save()
        return redirect('manager/request_production')
    
class Confirm_Production_:
    def main(request):
        producing = ProductInOrder.objects.filter(status="Producing")
        context = {"producing": producing}
        return render(request, "myproject/production/staff.html", context)
    
    def confirm_produce(request, order_id, product_type):
        pro_in_order = get_object_or_404(ProductInOrder, order_id=order_id, product_type=product_type)
        if request.method == 'POST':
            pro_in_order.status = "Produced"
            pro_in_order.save()
        return redirect('staff/confirm_production')
    