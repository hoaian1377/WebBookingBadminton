from django.shortcuts import render
from django.http import HttpResponse

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