from django.shortcuts import render, HttpResponse, redirect
from . import make_cars
from .models import *
import random


def gen_pics():
    name = ['Used 2014 BMW Gran Grey.jpg','Used 2015 BMW 335i Sedan Blue.jpg', 'Used 2015 BMW 335i Sedan Red.jpg', 'Used 2016 BMW Gran Grey.jpg']

    # pics = random.sample(name, 3)

    for i in name:
        new_car = Car.objects.create(name=i)  
    
