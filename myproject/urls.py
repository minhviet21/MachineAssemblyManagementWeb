from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name=""),
    path("manager", views.manager, name="manager"),
    path("staff", views.staff, name="staff"),
    path("manager/productcomponent", views.Product_Component.main, name="manager/productcomponent"),
    path("manager/productcomponent/<int:id>/", views.Product_Component.update, name="manager/productcomponent/id/"),
    path("manager/productcomponent/add", views.Product_Component.add, name="manager/productcomponent/add"),
    path("manager/componentinfor", views.Component_Infor.main, name="manager/componentinfor"),
    path("manager/componentinfor/<int:id>/", views.Component_Infor.update, name="manager/componentinfor/id/"),
    path("manager/componentinfor/add", views.Component_Infor.add, name="manager/componentinfor/add"),
]