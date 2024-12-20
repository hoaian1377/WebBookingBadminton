from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import RegisterForm
from .models import RegisterUser
# Create your views here.
def home(request):
    return render(request,'home.html')
def badminton_court_booking(request):
    return render(request,'badminton_court_booking.html')
def login(request):
    if request.method=='POST':
        username=request.POST.get('Username')
        password=request.POST.get('Password')
        try:
            user=RegisterUser.objects.get(Username=username,Password=password)
            return render(request,'home.html')
        except RegisterUser.DoesNotExist:
            return HttpResponse('Tên Đăng Nhập Hoặc Mật Khẩu Không Đúng')
    return render(request,'login.html')
def court_history(request):
    return render(request,'court_history.html')
def profile(request):
    return render(request,'profile.html')
def profile1(request):
    return render(request,'profile1.html')
def court_booking1(request):
    return render(request,'court_booking1.html')
def register(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})
def forgot_password(request):
    return render(request,'forgot_password.html')
def support(request):
    return HttpResponseRedirect("https://docs.google.com/forms/d/e/1FAIpQLSdsZGwFck63-cPDZcW8gZyyMAhf2UyYaOINuByEgwbMvtTm3A/viewform")
def shop(request):
    return render(request,'shop.html')
def item_detail(request):
    return render(request,'item_detail.html')
def cart_detail(request):
    return render(request,'cart_detail.html')
