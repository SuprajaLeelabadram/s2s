from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("view/<slug>/",views.ArtworkDetailView.as_view(),name="view"),
    path("cart/",views.cart,name="cart"),
    path("checkout/",views.checkout,name="checkout"),
    path("customize/",views.customize,name="customize"),
    path("update_item/",views.updateItem,name="update_item"),
    path("process_order/",views.processOrder,name="process_order"),
]
