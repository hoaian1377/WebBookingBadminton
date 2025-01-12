from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Products
# Create your views here.
def home(request):
    return render(request,'home.html')
def badminton_court_booking(request):
    return render(request,'badminton_court_booking.html')
def login(request):
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
    return render(request,'register.html')
def forgot_password(request):
    return render(request,'forgot_password.html')
def support(request):
    return HttpResponseRedirect("https://docs.google.com/forms/d/e/1FAIpQLSdsZGwFck63-cPDZcW8gZyyMAhf2UyYaOINuByEgwbMvtTm3A/viewform")
def shop(request):
    products = Products.objects.filter(isactive=True)  # Fetch active products
    return render(request, 'shop.html', {'products': products})
def item_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    return render(request, 'item_detail.html', {'product': product})
def cart_detail(request):
    return render(request,'cart_detail.html')
