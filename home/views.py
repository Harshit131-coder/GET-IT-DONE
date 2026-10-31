from django.contrib.auth import models
from django.shortcuts import get_object_or_404, render, reverse,redirect
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse, JsonResponse, request
from . models import Category, Services,cart, contact, Order, booking, Review,Faq,Rating
from django.contrib.auth.models import User 
from register.models import Pprofile
from django.contrib import messages
# Create your views here.
def index(request):
    cat=Category.objects.all()
    return render (request,"index.html",{"categ":cat})
def about(request):
    return render(request,"about.html")
def Contact(request):
    usr=contact.objects.filter(user__id=request.user.id)
    if request.method=="POST":
        phone=request.POST['phone']
        content=request.POST['content']
        print(phone, content)
        if len(phone)<10 or len(content)<4:
            messages.info(request, "Field Error")
        else:
            usr=get_object_or_404(User,id=request.user.id)
            con=contact(user=usr,phone=phone,msg=content)
            con.save()
            messages.info(request, "Message send successfully...")
    return render(request, "contact.html")        

def price(request):
    return render (request,"price.html")
def services(request,cid): 
    cat=Category.objects.get(id=cid)
    data=Services.objects.filter(cate=cat).order_by("id")
     
    return render (request, "services.html",{"data": data})

def service(request):
    
    data=Services.objects.all() 
    return render (request, "services.html",{"data": data})

def search(request):
    if request.method=="GET":
        se=request.GET["field"]
        ser=Services.objects.filter(name__icontains=se).order_by("id")
        return render(request,"services.html",{"data": ser})
def servicesone(request):
    pd={}
    if request.method=="POST":
        sid=request.POST["sid"]
        ser=Services.objects.get(id=sid)
       
        
        re=Rating.objects.filter(service=sid)
        rt=0
        for i in re:
            rt=rt+int(i.rate)/len(re)
        
        pd['data']=ser
        pd['rat']=re
        pd['rt']=rt
    return render(request, "services2.html",pd)
def Cart(request):
    dic={}
    item=cart.objects.filter(user__id=request.user.id,status=False)
    dic["item"]=item
    if request.user.is_authenticated:
     
        if request.method=="POST":
            sid=request.POST["srid"]
            quantity=request.POST["qty"]
            is_exist=cart.objects.filter(service_id=sid,user_id=request.user.id,status="False")
            if len(is_exist)>0:
                dic["msg"]="Item already exist in your cart."
            else:
                srvc=get_object_or_404(Services,id=sid)
                usr=get_object_or_404(User,id=request.user.id)
                crt=cart(user=usr,service=srvc,quantity=quantity)
                crt.save()
                dic["msg"]="{}Added in your cart.".format(srvc.name)
                dic["cls"]="alert alert success"
        else:
            dic["status"]="Please login first to view your cart."
    return render(request, "cart.html",dic)

def get_cart_data(request):
    item = cart.objects.filter(user__id=request.user.id, status=False)
    sale, quantity = 0, 0
    for i in item:
        sale += float(i.service.price)*i.quantity
        quantity = int(i.quantity)
    resp = {"quan": quantity, "tot": sale}
    return JsonResponse(resp)


def r_cart(request):
    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cartobj = get_object_or_404(cart, id=id)
        cartobj.delete()
    return HttpResponse(1)
def process_payment(request):
    item = cart.objects.filter(user_id__id=request.user.id, status=False)
    seri = ""
    amt = 0
    inv = "Skilled_hands Invoice"
    s_id = ""
    cart_id = ""
    for i in item:
        seri += str(i.service.name)+"/n"
        amt += float(i.service.price)
        inv += str(i.id)
        s_id += str(i.service.id)+","
        cart_id += str(i.id)+","
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amt/75),
        'item_name': seri,
        'invoice': inv,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",reverse('success_pay')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",reverse('cancel_pay')),
    }
    usr=User.objects.get(username=request.user.username)
    ord=Order(cust_id=usr,cart_ids=cart_id, product_ids=s_id)
    ord.save()
    ord.invoice_id=str(ord.id)+inv
    ord.save() 
    form=PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form}, )
def cancel_pay(request):
    return render(request, 'cancel_pay.html')
def success_pay(request):
     if "order_id" in request.session:
        order_id=request.session["order_id"]
        ord_obj=get_object_or_404(Order, id=order_id)
        ord_obj.status=True
        ord_obj.save()
        for i in ord_obj.cart_ids.split(",")[:-1]:
            cart_object=cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()
     return render(request, "success_pay.html")
def bookings(request):
    dic={}
    usr=User.objects.get(username=request.user.username)
    item=cart.objects.filter(user__id=request.user.id)
    dic["item"]=item
    cart_id=""
    for i in item:
        cart_id += str(i.id)+","    
    if request.method=="POST":
        add=request.POST["add"]
        purp=request.POST["purp"]
        phone=request.POST["phone"]
        time=request.POST["time"]
        date=request.POST["date"]
        v=booking(add=add,purp=purp,phone=phone,time=time,date=date,usr=usr)
        v.save()
        v.categ=cart_id
        v.save()
    return render(request,'booking.html')
    
def addser(request):
#aser = Profile.objects.filter(user__id=request.user.id)
    ad={}
    aser=Category.objects.all()
    ad["aser"]=aser
    provider = request.user
    if request.method == "POST":
        name = request.POST["ser_name"]
        c=request.POST["categ"]
        price = request.POST["price"]
        description = request.POST["desc"]
        #service_provider = Profile.objects.get(user__id=request.user.id)
        category=Category.objects.get(id=c)
        ap = Services(name=name, agent=provider,cate=category, price=price, desc=description)
        ap.save()
        if "img" in request.FILES:
            image=request.FILES["img"]
            ap.image=image
            ap.save()
            messages.info(request,"Image uploaded successfully")
        return redirect('services')

    return render(request, "addservice.html",{"aser":aser})

def faq(request):
    fq=Faq.objects.all().order_by("id")

    return render(request,"faq.html",{"data":fq})


