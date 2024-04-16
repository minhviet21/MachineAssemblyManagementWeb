from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name=""),
    path("productcomponent", views.productcomponent, name="productcomponent"),
    path("productcomponent/<int:id>/", views.updateproductcomponent, name="productcomponent/id/"),
]