from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="2"),
    path("productcomponent", views.productcomponent, name="3"),
]