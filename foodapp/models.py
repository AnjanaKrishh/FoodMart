from django.db import models

# Create your models here.
class reg(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    image = models.FileField(upload_to='image/')

class product(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(upload_to='media/',null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
   
class sellerproduct(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(upload_to='media/',null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.name

class cart(models.Model):
    user = models.ForeignKey(reg,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(null=True,blank=True)
    def _str_(self):
        return f"cart of{self.user.name}"
    

class buy(models.Model):
    user = models.ForeignKey(reg, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    address = models.TextField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

class sreg(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    image = models.FileField(upload_to='image/')
    phone = models.IntegerField(null=True,blank=True)
    shopname = models.CharField(max_length=20,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
 
class feedbacks(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    rating = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return self.name

    