from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
     cat_name = models.CharField(max_length=250)
     cover_pic = models.FileField(upload_to="cat_pics")
     description = models.TextField()
     added_on =models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return self.cat_name   
class Services(models.Model):
    name=models.CharField(max_length=50)
    agent=models.ForeignKey(User,on_delete=models.CASCADE)
    desc=models.TextField(blank=True)
    cate=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.IntegerField()
    image=models.ImageField(upload_to="pics")

    
    def __str__(self):
        return self.name
class cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    status=models.BooleanField(default=False)
    service=models.ForeignKey(Services, on_delete=models.CASCADE)
    added_on=models.DateTimeField(auto_now_add=True, null=True)
    update_on=models.DateTimeField(auto_now=True, null=True)

    def _str_(self):
        return self.user.username    
class contact(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.BigIntegerField()
    msg=models.TextField()
    subj=models.CharField(max_length=50)
    addon=models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return self.user.username  
class Order(models.Model):
    cust_id = models.ForeignKey(User,on_delete=models.CASCADE)
    cart_ids = models.CharField(max_length=250)
    product_ids = models.CharField(max_length=250)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cust_id.username  
duration=(("7:00am","7:00am"),("9:00am","9:00am"),("11:00am","11:00am"),("1:00pm","1:00pm"),("5:00pm","5:00pm"))
class booking(models.Model):
    add=models.CharField(max_length=250)
    date=models.DateTimeField(auto_now_add=True)
    time=models.CharField(choices=duration,max_length=25)
    purp=models.CharField(max_length=250)
    phone=models.BigIntegerField(max_length=10)
    categ=models.CharField(max_length=250)
    usr=models.ForeignKey(User,on_delete=models.CASCADE)
    def _str_(self):
        return self.name
class Review(models.Model):
    product = models.ForeignKey(Services, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    subject = models.CharField(max_length=50)
    review = models.CharField(max_length=200)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name + " by " + self.user.first_name
 
class Faq(models.Model):
    questions = models.TextField()
    answers = models.TextField()
    def __str__(self):
        return self.questions

rate=(("1","Worst"),("2","Bad"),("3","Good"),("4","Very Good"),("5","Excellent"))
class Rating(models.Model):
    rate=models.CharField(choices=rate,max_length=25,default="Good",blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    service =models.ForeignKey(Services,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    
