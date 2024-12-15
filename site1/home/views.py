from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def home(request):
    return render(request,'home.html')
def badminton_court_booking(request):
    return render(request,'badminton_court_booking.html')
def login(request):
    return render(request,'login.html')
def court_history(request):
    return render(request,'court_history.html')
def court_booking1(request):
    return render(request,'court_booking1.html')
def register(request):
    return render(request,'register.html')
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
