from django.shortcuts import render
from django.http import HttpResponse
from .models import ProductComponent

def index(request):
    list_product = ProductComponent.objects.all()
    context = {"list_product": list_product}
    return render(request, "myproject/index.html", context)

def show_table(request):
    list_product = ProductComponent.objects.all()
    output = "<table>"
    output += "<tr><th>ID</th><th>Product Type</th><th>Component Type</th><th>Quantity</th></tr>"
    for product in list_product:
        output += "<tr>"
        output += "<td>{}</td>".format(product.id)
        output += "<td>{}</td>".format(product.product_type)
        output += "<td>{}</td>".format(product.component_type)
        output += "<td>{}</td>".format(product.quantity)
        output += "</tr>"
    output += "</table>"
    return HttpResponse(output)