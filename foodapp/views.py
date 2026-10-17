from django.shortcuts import render,HttpResponse,redirect
from .import models
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.
def index(request):
    return render(request,'index.html')
def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        age=request.POST.get('age')
        email=request.POST.get('email')
        password=request.POST.get('password')
        image=request.FILES.get('image')
        if models.reg.objects.filter(email=email).exists():
            alert="<script>alert('email already exist'); window.location.href='/register/';</script>;"
            return HttpResponse(alert)
        else:
            user=models.reg(name=name,age=age,email=email,password=password,image=image)
            user.save()
            return redirect('login')
    else:
        return render(request,'register.html')

def loginpage(request):
    if request.method == "POST":
        # Step 1: Initial Login Phase
        if 'email' in request.POST and 'password' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = models.reg.objects.get(email=email, password=password)
                # Generate OTP
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                request.session['email'] = user.email

                # Send OTP via Email
                send_mail(
                    'Your Login OTP',
                    f'Your OTP is {otp}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return render(request, 'verifyotp.html', {'msg': 'OTP sent to your email.'})
            except models.reg.DoesNotExist:
                msg = "Invalid email or password"
                return render(request, 'login.html', {'msg': msg})

        # Step 2: OTP Verification Phase
        if 'verifyotp' in request.POST:
            otp = request.POST.get('otp')
            if str(request.session.get('otp')) == otp:
                # OTP matches, log the user in
                return redirect('profile')  # Redirect to profile 
            else:
                return render(request, 'verifyotp.html', {'msg': 'Invalid OTP'})

    return render(request, 'login.html')
    
def home(request):
    return render(request,'home.html')


def profile(request):
    if "email" in request.session:
        user = request.session['email']
        try:
            client = models.reg.objects.get(email=user)
            return render(request, 'profile.html', {'c': client})   
        except models.reg.DoesNotExist:
            alert = "<script>alert('user not found'); window.location.href='/login/';</script>"
            return HttpResponse(alert)
    else:    
        alert = "<script>alert('user not found'); window.location.href='/login/';</script>"  
        return HttpResponse(alert)

    
    
def editprofile(request):
    if "email" in request.session:
        user=request.session['email']
        try:
            client=models.reg.objects.get(email=user)
            if request.method=='POST':
                client.name=request.POST.get('name')
                client.age=request.POST.get('age')
                client.email=request.POST.get('email')
                client.password=request.POST.get('password')
                image=request.FILES.get('image')
                if image :
                    client.image=image
                client.save()
                return redirect('profile')
            else:
                return render(request, 'editprofile.html', {'c': client})
        except models.reg.DoesNotExist:
            alert = "<script>alert('user not found'); window.location.href='/login/';</script>"
            return HttpResponse(alert)
    else:
        alert = "<script>alert('user not found'); window.location.href='/login/';</script>"
        return HttpResponse(alert)
    
def adminlogin(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        upassword=request.POST.get('upassword')
        auname="ADMIN"
        apassword="admin"
        if auname==uname:
            if apassword==upassword:
                return redirect('adhome')
            else:
                return redirect('adminlogin')
        else:
            return redirect('adminlogin')
    else:
        return render(request,'adminlogin.html')
    
def adhome(request):
    return render(request,'adhome.html')

def userlist(request):
    user=models.reg.objects.all()
    return render(request,'userlist.html',{'u':user})

def deleteuser(request,id):
    user=models.reg.objects.filter(id=id)
    user.delete()
    return redirect('userlist')

def logout(request):
    if 'email'in request.session:
        request.session.flush()
        return redirect('index')
    else:
        return redirect('index')
    
def addproduct(request):
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        image=request.FILES.get('image')
        quantity=request.POST.get('quantity')
        price=request.POST.get('price')
        user=models.product(name=name,description=description,image=image,quantity=quantity,price=price,)
        user.save()
        return redirect('productlist')
    else:
        return render(request,'addproduct.html')
    
def productlist(request):
    user=models.product.objects.all()
    return render(request,'productlist.html',{'a':user})

def deleteproduct(request,id):
    user=models.product.objects.get(id=id)
    user.delete()
    return redirect('productlist')
    
def editproduct(request,id):
    client=models.product.objects.get(id=id)
    if request.method=='POST':
        client.name=request.POST.get('name')
        client.description=request.POST.get('description')
        client.quantity=request.POST.get('quantity')
        client.price=request.POST.get('price')
        image=request.FILES.get('image')
        if image :
            client.image=image
        client.save()
        return redirect('productlist')
    else:
        return render(request, 'editproduct.html', {'c': client})
    
def userproductlist(request):
      user=models.product.objects.all()
      return render(request,'userproductlist.html',{'a':user})
  
def addcart(request, id):
    if "email" in request.session:
        user = request.session['email']
        client = models.reg.objects.get(email=user)
        product = models.product.objects.get(id=id)

        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))

            cart_item, created = models.cart.objects.get_or_create(
                user=client,
                product=product,
                defaults={'quantity': quantity, 'total_price': product.price * quantity}
            )

            if not created:
                cart_item.quantity = quantity
                cart_item.total_price = product.price * quantity
                cart_item.save()
                
            return redirect('cartlist')
                   
        
        else:
            return render(request, 'addcart.html', {'p': product})
    else:
        return redirect('login')



def cartlist(request):
    if "email" in request.session:
        user = request.session['email']
        client = models.reg.objects.get(email=user)
        cart_items = models.cart.objects.filter(user=client)  # Use filter, not get

        return render(request, 'cartlist.html', {'cart_items': cart_items})
    else:
        return redirect('index')  # Make sure 'login' is a valid URL name



def deletecartitem(request, id):
    if "email" in request.session:
        user = request.session['email']
        client = models.reg.objects.get(email=user)
        cart_item = models.cart.objects.get(id=id, user=client)
        cart_item.delete()
        return redirect('cartlist')
    else:
        return redirect('index')
    
def buynow(request, id):
    user = request.session.get('email')
    if user:
        client = models.reg.objects.get(email=user)
        product = models.product.objects.get(id=id)
        
        if request.method == 'POST':
            address = request.POST.get('address')
            phone = request.POST.get('phone')

            buy_item = models.buy(user=client, product=product, address=address, phone=phone)
            buy_item.save()
            return redirect('paylist')
        else:
            return render(request, 'buynow.html', {'user': client, 'product': product})
    else:
        return redirect('login')


def paylist(request):
    if "email" in request.session:
        user = request.session['email']
        client = models.reg.objects.get(email=user)
        buy_items = models.buy.objects.filter(user=client)

        return render(request, 'paylist.html', {'buy_items': buy_items})
    else:
        return redirect('login')
    
def sellregister(request):
    if request.method=='POST':
        name=request.POST.get('name')
        age=request.POST.get('age')
        email=request.POST.get('email')
        password=request.POST.get('password')
        image=request.FILES.get('image')
        phone=request.POST.get('phone')
        shopname=request.POST.get('shopname')
        address=request.POST.get('address')
        if models.sreg.objects.filter(email=email).exists():
            alert="<script>alert('email already exist'); window.location.href='/register/';</script>;"
            return HttpResponse(alert)
        else:
            user=models.sreg(name=name,age=age,email=email,password=password,image=image)
            user.save()
            return redirect('selllogin')
    else:
        return render(request,'sellregister.html')
    
    
def selllogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=models.sreg.objects.get(email=email)
            if user.password==password:
                request.session['email']=email
                return redirect('sellhome')
            else:
                alert="<script>alert('invalid user'); window.location.href='/selllogin/';</script>;"
                return HttpResponse(alert)
        except models.sreg.DoesNotExist:
            alert="<script>alert('user not found'); window.location.href='/selllogin/';</script>;"
            return HttpResponse(alert)
    else:
        return render(request,'selllogin.html')


def sellhome(request):
    return render(request,'sellhome.html')

def sellprofile(request):
    if "email" in request.session:
        user = request.session['email']
        try:
            client = models.sreg.objects.get(email=user)
            return render(request, 'sellprofile.html', {'c': client})   
        except models.sreg.DoesNotExist:
            alert = "<script>alert('user not found'); window.location.href='/sellprofile/';</script>"
            return HttpResponse(alert)
    else:    
        alert = "<script>alert('user not found'); window.location.href='/selllogin/';</script>"  
        return HttpResponse(alert)
    



# def sellproduct(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         image = request.FILES.get('image')
#         quantity = request.POST.get('quantity')
#         price = request.POST.get('price')
        
#         # Cast quantity and price if needed
#         product = models.sellerproduct(
#             name=name,
#             description=description,
#             image=image,
#             quantity=quantity,
#             price=price
#         )
#         product.save()
#         return redirect('sproductlist')
#     else:
#         return render(request, 'sellproduct.html')

    

# def sproductlist(request):
#     products = models.sellerproduct.objects.all()  # or filter as needed
#     return render(request, 'sproductlist.html', {'products': products})

def sale(request):
    return render(request,'sale.html')

def blog(request):
    return render(request,'blog.html')


from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models

from django.contrib import messages  # import messages

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        rating = request.POST.get('rating')

        user=models.feedbacks(
            name=name,
            email=email,
            message=message,
            rating=rating
        )
        user.save()

        # messages.success(request, '✅ Thank you! Your feedback has been submitted.')
        return redirect('feedbacklist')

    return render(request, 'feedback.html')


    


def feedbacklist(request):
    feedbacks = models.feedbacks.objects.all()
    return render(request,'feedbacklist.html', {'feedbacks': feedbacks})


def verifyotp(request):
    return render(request, 'verifyotp.html')