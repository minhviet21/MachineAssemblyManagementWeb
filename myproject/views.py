from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ProductComponent, ComponentInfor, OrderInfor, ProductInOrder, ComponentQuantity

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
            quantity = request.POST.get('quantity')
            if int(quantity) > 0:
                pro_com = ProductComponent(product_type=product_type, component_type=component_type, quantity=quantity)
                pro_com.save()
            return redirect('manager/productcomponent')
        else:
            pro_com = None
        return render(request, "myproject/productcomponent/add.html", {'pro_com': pro_com})

class Component_Infor:
    def main(request):
        list_com_infor = ComponentInfor.objects.all()
        context = {"list_com_infor": list_com_infor}
        return render(request, "myproject/componentinfor/main.html", context)

    def update(request, id):
        com_infor = get_object_or_404(ComponentInfor, id=id)
        if request.method == 'POST':
            supplier_name = request.POST.get('supplier_name')
            supplier_address = request.POST.get('supplier_address')
            if supplier_name == '' or supplier_address == '':
                com_infor.delete()
            else:
                com_infor.supplier_name = supplier_name
                com_infor.supplier_address = supplier_address
                com_infor.save()
            return redirect('manager/componentinfor')
        return render(request, "myproject/componentinfor/update.html", {'com_infor': com_infor})

    def add(request):
        if request.method == 'POST':
            component_type = request.POST.get('component_type')
            supplier_name = request.POST.get('supplier_name')
            supplier_address = request.POST.get('supplier_address')
            com_infor = ComponentInfor(component_type=component_type, supplier_name=supplier_name, supplier_address=supplier_address)
            com_infor.save()
            return redirect('manager/componentinfor')
        else:
            com_infor = None
        return render(request, "myproject/componentinfor/add.html", {'com_infor': com_infor})