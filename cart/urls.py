from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.summary, name="cart__summary"),
    path("add/", views.add, name="cart__add"),
    path("delete/", views.delete, name="cart__delete"),
    path("update/", views.update, name="cart__update"),
]
