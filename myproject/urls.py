from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="2"),
    path("show_table", views.show_table, name="3"),
]