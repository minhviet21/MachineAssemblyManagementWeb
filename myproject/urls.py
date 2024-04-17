from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name=""),
    path("manager", views.manager, name="manager"),
    path("staff", views.staff, name="staff"),
    path("manager/productcomponent", views.productcomponent, name="manager/productcomponent"),
    path("manager/productcomponent/<int:id>/", views.updateproductcomponent, name="manager/productcomponent/id/"),
    path("manager/productcomponent/add", views.addproductcomponent, name="manager/productcomponent/add"),
]