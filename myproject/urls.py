from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="homepage"),
    path("manager", views.manager, name="manager"),
    path("staff", views.staff, name="staff"),


    path("manager/product", views.Product_.main, name="manager/product"),
    path("manager/product/add_product", views.Product_.add_product, name="manager/product/add_product"),
    path("manager/product/<str:product_type>/", views.Product_.show_component, name="manager/product/product_type"),
    path("manager/product/<str:product_type>/add_component", views.Product_.add_component, name="manager/product/product_type/add_component"),
    path("manager/product/<str:product_type>/update_product", views.Product_.update_product, name="manager/product/product_type/update_product"),
    path("manager/product/<str:product_type>/<str:component_type>", views.Product_.update_component, name="manager/product/product_type/component_type"),
    

    path("manager/component", views.Component_.main, name="manager/component"),
    path("manager/component/<str:component_type>/", views.Component_.update, name="manager/component/component_type"),
    path("manager/component/add", views.Component_.add, name="manager/component/add"),
    

    path("manager/request_production", views.Request_Production_.main, name="manager/request_production"),
    path("manager/request_production/<int:order_id>/<str:product_type>/", views.Request_Production_.request_production, name="manager/request_production"),
    
    path("staff/order", views.Order_.main, name="staff/order"),
    path("staff/order/add_order", views.Order_.add_order, name="staff/order/add_order"),
    path("staff/order/<int:order_id>/show_product", views.Order_.show_product, name="staff/order/order_id/show_product"),
    path("staff/order/<int:order_id>/update_order", views.Order_.update_order, name="staff/order/order_id/update_order"),
    path("staff/order/<int:order_id>/add_product", views.Order_.add_product, name="staff/order/order_id/add_product"),
    path("staff/order/<int:order_id>/<str:product_type>", views.Order_.update_product, name="staff/order/order_id/product_type"),

    path("manager/quantity", views.Quantity_.main, name="manager/quantity"),
    path('manager/quantity/add', views.Quantity_.add, name='manager/quantity/add'),
    #path('manager/quantity/show/<str:component_type>', views.Quantity_.show, name='quantity/show'),

    path("staff/supply", views.Supply_.main, name="staff/supply"),
    path('staff/supply/send', views.Supply_.send, name='staff/supply/send'),
    
    path("staff/confirm_production", views.Confirm_Production_.main, name="staff/confirm_production"),
    path("staff/confirm_production/<int:order_id>/<str:product_type>/", views.Confirm_Production_.confirm_produced, name="staff/confirm_production"),
]