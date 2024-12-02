from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'home.html')
def badminton_court_booking(request):
    return render(request,'badminton_court_booking.html')
def login(request):
    return render(request,'login.html')