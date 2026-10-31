from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from home.models import contact,Services,Rating
from .models import Pprofile
# Create your views here.
def register(request):
    if(request.method=='POST'):
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        email=request.POST['email']
        user_name=request.POST['uname']
        password=request.POST['pass']
        conf_password=request.POST['cnfpass']   
        aadhar=request.POST['aadhar']             
        if(password==conf_password):
            if User.objects.filter(username=user_name).exists():
                messages.info(request,"Oops! username already taken.. ")
                return redirect ("reg")
            else:
                user= User.objects.create_user(username=user_name,first_name=first_name,last_name=last_name,email=email,password=password)
                user.save()  
                user2 = Pprofile(user=user, aadhar=aadhar)
                user2.save()
                messages.info(request,"User created successfully")
                return redirect('login')
    return render(request,"reg.html")
def staffreg(request):
    if(request.method=='POST'):
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        email=request.POST['email']
        user_name=request.POST['uname']
        password=request.POST['pass']
        conf_password=request.POST['cnfpass']
        aadhar=request.POST['aadhar']
        category=request.POST['category']
        if (password == conf_password):
            if User.objects.filter(username=user_name).exists():
                 messages.info(request, "Oops! Username already taken.")
                 return redirect("staffreg")
            else:
                user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name, email=email, password=password)
                if "staff" in request.POST:
                    user.is_staff=True
                    user.save()
                user2 = Pprofile(user=user, aadhar=aadhar,category=category )
                user2.save()
                messages.info(request, "Congrats you are in..")
                return redirect('login')
    return render(request, "staffreg.html")
def login (request):
    if (request.method=="POST"):
        user_name=request.POST["user_name"]
        password=request.POST["password"]
        logger=auth.authenticate(username=user_name, password=password)
        if logger!=None:
            auth.login(request,logger)
            return redirect("index")
        else:
            return redirect("login")
    else:
        return render(request,"login.html")
    
           
def logout(request):
    auth.logout(request)
    return redirect("index")
def profile(request):
    display={}
    usr=get_object_or_404(User,id=request.user.id)
    prof=Pprofile.objects.filter(user__id=request.user.id)
    if len(prof)>0:
        dis=Pprofile.objects.get(user__id=request.user.id)
        display["data"]=dis
        x=contact.objects.filter(user__id=request.user.id)
        display["x"]=x
        if len(x)>0:
            con=contact.objects.filter(user__id=request.user.id)
        sers=Services.objects.all()
        display["sers"]=sers
        if request.method=="POST":
            rate=request.POST["rate"]
            ser=request.POST["ser"]
            serv=Services.objects.get(id=ser)
            re=Rating(user=usr,rate=rate,service=serv)
            re.save()
        

    return render(request,"team-details.html",display)
def update_profile(request):
    display={}
    prof=Pprofile.objects.filter(user__id=request.user.id)
    if len(prof)>0:
        dis=Pprofile.objects.get(user__id=request.user.id)
        display["data"]=dis
        if request.method=="POST":
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email=request.POST["email"]
            con=request.POST["cont_no"]
            pin=request.POST["pin"]
            add=request.POST["address"]
            st=request.POST["state"]
            city=request.POST["city"]
            gender=request.POST["gender"]
            aadhar=request.POST["aadhar"]
            up_user=User.objects.get(id=request.user.id)
            up_user.first_name=fname
            up_user.last_name=lname
            up_user.email=email
            up_user.save()
            dis.pin=pin
            dis.add=add
            dis.state=st
            dis.cont_no=con
            dis.city=city
            dis.gender=gender
            dis.aadhar=aadhar
            dis.save()
            if "img" in request.FILES:
                image=request.FILES["img"]
                dis.pfp=image
                dis.save()
                messages.info(request,"Image uploaded successfully")
            messages.info(request,"Profile uploaded successfully") 
            
        


            
        
    return render(request,"update_profile.html",display)


            