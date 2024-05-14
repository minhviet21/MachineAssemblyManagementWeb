from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ProductComponent, Component, Order, ProductInOrder, ComponentQuantity, Product
from .forms import OrderForm
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
            if not (Product.objects.filter(product_type=product_type).exists()) and product_type != '':
                product = Product(product_type=product_type)
                product.save()
            return redirect('manager/product')
        return render(request, "myproject/product/add_product.html")

    def update_product(request, product_type):
        product = get_object_or_404(Product, product_type=product_type)
        if request.method == 'POST':
            product_type = request.POST.get('product_type')
            if product_type == '':
                ProductComponent.objects.filter(product_type=product.product_type).delete()
                product.delete()
            elif Product.objects.filter(product_type=product_type).exists():
                return redirect('manager/product')
            else:
                ProductComponent.objects.filter(product_type=product.product_type).update(product_type=product_type)
                product.product_type = product_type
                product.save()
            return redirect('manager/product')
        return render(request, "myproject/product/update_product.html", {'product': product})

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

class Quantity_:
    def main(request):
        list_quantity = ComponentQuantity.objects.all()
        return render(request, "myproject/quantity/main.html", {'list_quantity': list_quantity})

    def add(request):
        if request.method == "POST":
            component_type = request.POST.get('component_type')
            number = int(request.POST.get('number'))
            component, created = ComponentQuantity.objects.get_or_create(component_type=component_type, defaults={'now': 0, 'supplying': number, 'need': 0})
            if not created:
                component.supplying += number
                component.save()
            return redirect('manager/quantity')
        return render(request, "myproject/quantity/add.html")

    
class Supply_:
    def main(request):
        list_quantity = ComponentQuantity.objects.all()
        return render(request, "myproject/supply/main.html", {'list_quantity': list_quantity})

    def send(request):
        if request.method == "POST":
            component_type = request.POST.get('component_type')
            number = int(request.POST.get('number'))
            component, created = ComponentQuantity.objects.get_or_create(component_type=component_type, defaults={'now': 0, 'supplying': number, 'need': 0})
            if not created:
                component.supplying += number
                component.save()
            return redirect('manager/quantity')
        return render(request, "myproject/quantity/add.html")

