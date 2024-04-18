from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name=""),
    path("manager", views.manager, name="manager"),
    path("staff", views.staff, name="staff"),

    path("manager/product", views.Product_.main, name="manager/product"),
    path("manager/product/add_product", views.Product_.add_product, name="manager/product/add_product"),
    path("manager/product/<str:product_type>/", views.Product_.show_component, name="manager/product/product_type"),
    path("manager/product/<str:product_type>/add_component", views.Product_.add_component, name="manager/product/product_type/add_component"),
    path("manager/product/<str:product_type>/<str:component_type>", views.Product_.update_component, name="manager/product/product_type/component_type"),

    path("manager/component", views.Component_.main, name="manager/component"),
    path("manager/component/<str:component_type>/", views.Component_.update, name="manager/component/component_type"),
    path("manager/component/add", views.Component_.add, name="manager/component/add"),
    path("staff/order", views.Order_.main, name="staff/order"),
]