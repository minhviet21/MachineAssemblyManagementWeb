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
            else:
                return render(request, "myproject/product/add_product.html")
        return render(request, "myproject/product/add_product.html")

    def update_product(request, product_type):
        product = get_object_or_404(Product, product_type=product_type)
        if request.method == 'POST':
            product_type = request.POST.get('product_type')
            if product_type == '':
                ProductComponent.objects.filter(product_type=product.product_type).delete()
                product.delete()
            elif Product.objects.filter(product_type=product_type).exists():
                return render(request, "myproject/product/update_product.html", {'product': product})
            else:
                ProductComponent.objects.filter(product_type=product.product_type).update(product_type=product_type)
                ProductInOrder.objects.filter(product_type=product.product_type).update(product_type=product_type)
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
        list_component = Component.objects.all()
        list_component_in_product = ProductComponent.objects.filter(product_type=product.product_type)
        list_component_not_in_product = list_component.exclude(component_type__in=[pro_com.component_type for pro_com in list_component_in_product])
        if request.method == 'POST':
            component_type = request.POST.get('component_type')
            quantity = request.POST.get('quantity')
            if int(quantity) > 0 \
                and (not ProductComponent.objects.filter(product_type=product.product_type, component_type=component_type).exists()):
                # update need of component
                component_quantity = get_object_or_404(ComponentQuantity, component_type=component_type)
                product_in_order = ProductInOrder.objects.filter(product_type=product.product_type)
                component_quantity.need += len(product_in_order) * int(quantity)
                component_quantity.miss = max(0, component_quantity.need - component_quantity.now - component_quantity.supplying)
                component_quantity.save()
                pro_com = ProductComponent(product_type=product.product_type, component_type=component_type, quantity=quantity)
                pro_com.save()
                return redirect(reverse('manager/product/product_type', kwargs={'product_type': product_type}))
            else:
                pro_com = None
                return render(request, "myproject/product/add_component.html", {'pro_com': pro_com, 'product': product, 'list_component_not_in_product': list_component_not_in_product})
        else:
            pro_com = None
        return render(request, "myproject/product/add_component.html", {'pro_com': pro_com, 'product': product, 'list_component_not_in_product': list_component_not_in_product})

    def update_component(request, product_type, component_type):
        pro_com = get_object_or_404(ProductComponent, product_type=product_type, component_type=component_type)
        if request.method == 'POST':
            quantity = request.POST.get('quantity')
            component_quantity = get_object_or_404(ComponentQuantity, component_type=component_type)
            if int(quantity) <= 0:
                component_quantity = get_object_or_404(ComponentQuantity, component_type=component_type)
                product_in_order = ProductInOrder.objects.filter(product_type=product_type)
                component_quantity.need -= len(product_in_order) * pro_com.quantity
                component_quantity.miss = max(0, component_quantity.need - component_quantity.now - component_quantity.supplying)
                component_quantity.save()
                pro_com.delete()
            else:
                component_quantity = get_object_or_404(ComponentQuantity, component_type=component_type)
                product_in_order = ProductInOrder.objects.filter(product_type=product_type)
                component_quantity.need += len(product_in_order) * (int(quantity) - pro_com.quantity)
                component_quantity.miss = max(0, component_quantity.need - component_quantity.now - component_quantity.supplying)
                component_quantity.save()
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
                component_quantity = ComponentQuantity.objects.filter(component_type=component.component_type)
                component_quantity.delete()
                product_component = ProductComponent.objects.filter(component_type=component.component_type)
                product_component.delete()
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
            if not (Component.objects.filter(component_type=component_type).exists()) and component_type != '':
                component = Component(component_type=component_type, supplier_name=supplier_name, supplier_address=supplier_address)
                component.save()
                component_quantity = ComponentQuantity(component_type=component.component_type, now=0, supplying=0, need=0)
                component_quantity.save()
                return redirect('manager/component')
            else:
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
                product_in_order = ProductInOrder.objects.filter(order_id=order.order_id)
                for pro_in_order in product_in_order:
                    product_component = ProductComponent.objects.filter(product_type=pro_in_order.product_type)
                    for pro_com in product_component:
                        component = get_object_or_404(ComponentQuantity, component_type=pro_com.component_type)
                        component.need -= pro_com.quantity*pro_in_order.quantity
                        component.save()
                    pro_in_order.delete()
                ProductInOrder.objects.filter(order_id=order.order_id).delete()
                order.delete()
            elif phone_number == '' or not phone_number.isdigit():
                return render(request, "myproject/order/update_order.html", {'order': order})    
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
        list_product = Product.objects.all()
        list_product_in_order = ProductInOrder.objects.filter(order_id=order.order_id)
        list_product_not_in_order = list_product.exclude(product_type__in=[pro_in_order.product_type for pro_in_order in list_product_in_order])
        if request.method == 'POST':
            product_type = request.POST.get('product_type')
            quantity = request.POST.get('quantity')
            if Product.objects.filter(product_type=product_type).exists() and int(quantity) > 0:
                pro_in_order = ProductInOrder(order_id=order.order_id, product_type=product_type, quantity=int(quantity), status="Not produced")
                pro_in_order.save()
                product_component = ProductComponent.objects.filter(product_type=product_type)
                for pro_com in product_component:
                    component = get_object_or_404(ComponentQuantity, component_type=pro_com.component_type)
                    component.need += pro_com.quantity*pro_in_order.quantity
                    component.save()
                return redirect(reverse('staff/order/order_id/show_product', kwargs={'order_id': order_id}))
            else:
                pro_in_order = None
                return render(request, "myproject/order/add_product.html", {'pro_in_order': pro_in_order, 'order': order, 'list_product_not_in_order': list_product_not_in_order})
        else:
            pro_in_order = None
        return render(request, "myproject/order/add_product.html", {'pro_in_order': pro_in_order, 'order': order, 'list_product_not_in_order': list_product_not_in_order})

    def update_product(request, order_id, product_type):
        pro_in_order = get_object_or_404(ProductInOrder, order_id=order_id, product_type=product_type)
        if request.method == 'POST':
            quantity = request.POST.get('quantity')
            if int(quantity) <= 0:
                product_component = ProductComponent.objects.filter(product_type=pro_in_order.product_type)
                for pro_com in product_component:
                    component = get_object_or_404(ComponentQuantity, component_type=pro_com.component_type)
                    component.need -= pro_com.quantity*pro_in_order.quantity
                    component.save()
                pro_in_order.delete()
            else:
                product_component = ProductComponent.objects.filter(product_type=pro_in_order.product_type)
                for pro_com in product_component:
                    component = get_object_or_404(ComponentQuantity, component_type=pro_com.component_type)
                    component.need += (int(quantity) - pro_in_order.quantity)*pro_com.quantity
                    component.save()
                pro_in_order.quantity = quantity
                pro_in_order.save()
            return redirect(reverse('staff/order/order_id/show_product', kwargs={'order_id': order_id}))
        return render(request, "myproject/order/update_product.html", {'pro_in_order': pro_in_order})

class Quantity_:
    def main(request):
        list_quantity = ComponentQuantity.objects.all()
        return render(request, "myproject/quantity/main.html", {'list_quantity': list_quantity})

    def add(request):
        list_component = Component.objects.all()
        if request.method == "POST":
            component_type = request.POST.get('component_type')
            number = int(request.POST.get('number'))
            component, created = ComponentQuantity.objects.get_or_create(component_type=component_type, defaults={'now': 0, 'supplying': number, 'need': 0})
            if not created:
                component.supplying += number
                component.miss = max(0, component.need - component.now - component.supplying)
                component.save()
            return redirect(reverse('manager/quantity'), kwargs = {'list_component': list_component})
        return render(request, "myproject/quantity/add.html", {'list_component': list_component})
    
class Supply_:
    def main(request):
        list_quantity = ComponentQuantity.objects.all()
        return render(request, "myproject/supply/main.html", {'list_quantity': list_quantity})

    def send(request):
        list_component = Component.objects.all()
        if request.method == "POST":
            component_type = request.POST.get('component_type')
            number = int(request.POST.get('number'))
            component = get_object_or_404(ComponentQuantity, component_type=component_type)
            if number > component.supplying:
                return render(request, "myproject/supply/send.html", {'list_component': list_component})
            else:
                component.supplying -= number
                component.now += number
                component.save()
            return redirect('staff/supply')
        return render(request, "myproject/supply/send.html", {'list_component': list_component})

class Request_Production_:
    def main(request):
        ready_to_produce = Request_Production_.list_ordered_product()
        context = {"ready_to_produce": ready_to_produce}
        return render(request, "myproject/production/manager_request.html", context)

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
        return render(request, "myproject/production/staff_confirm.html", context)
    
    def confirm_produced(request, order_id, product_type):
        pro_in_order = get_object_or_404(ProductInOrder, order_id=order_id, product_type=product_type)
        if request.method == 'POST':
            pro_in_order.status = "Produced"
            pro_in_order.save()
        return redirect('staff/confirm_production')
