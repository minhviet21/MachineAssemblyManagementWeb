from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name=""),
    path("manager", views.manager, name="manager"),
    path("staff", views.staff, name="staff"),
    path("manager/productcomponent", views.Product_Component.main, name="manager/productcomponent"),
    path("manager/productcomponent/<int:id>/", views.Product_Component.update, name="manager/productcomponent/id/"),
    path("manager/productcomponent/add", views.Product_Component.add, name="manager/productcomponent/add"),
    path("manager/component", views.Component_.main, name="manager/component"),
    path("manager/component/<int:id>/", views.Component_.update, name="manager/component/id/"),
    path("manager/component/add", views.Component_.add, name="manager/component/add"),
]