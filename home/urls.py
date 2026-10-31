from django.urls import path
from . import views


urlpatterns = [
    path("",views.index, name="index"),
    path ("about",views.about, name="about"),
    path("price",views.price, name="price"),
    path("contact",views.Contact, name="contact"),
    path("services/<int:cid>",views.services, name="serv"),
    path("servicesone ",views.servicesone,name="servicesone"),
    path("search",views.search,name="search"),
    path("services",views.service, name='services'),
    path("cart",views.Cart, name='cart'),
    path("r_cart",views.r_cart,name="r_cart"),
    path("get_cart_data",views.get_cart_data,name="get_cart_data"),
    path("success_pay",views.success_pay,name="success_pay"),
    path("cancel_pay",views.cancel_pay,name="cancel_pay"),
    path("process_payment",views.process_payment,name="process_payment"),
    path("booking",views.bookings,name="booking"),
    path("review",views.Review,name="review"),
    path("addser",views.addser,name="addser"),
    path("faq",views.faq,name="faq"), 
] 