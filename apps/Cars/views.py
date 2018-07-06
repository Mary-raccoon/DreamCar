from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from django.core import serializers
import json
from django.db.models import Q

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags="login")
        return redirect('/')
    user =User.objects.get(email = request.POST['email1'])
    if(bcrypt.checkpw(request.POST['password1'].encode(), user.password.encode())):
        print("password match")
        # user = User.objects.get(email=request.POST['email1'])
        request.session['id']=user.id
        request.session['name'] = user.name
        request.session['email'] = user.email
        messages.success(request, "You successfully loged in")
        return redirect('/main')
    else:
        print("wrong password")
        return redirect('/')
    print(user.first_name)
   
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for field, msg in errors.items():
            messages.error(request, msg, extra_tags=field)
        return redirect('/')
    else:
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hash_password)
        user = User.objects.create(
            name=request.POST['name'],  
            email=request.POST['email'],
            password = hash_password
        )
        request.session['name'] = user.name
        messages.success(request, "User successfully created")
        
        return redirect('/main')

def index(request):
    return render(request, 'cars/index.html')

def search(request):
    return redirect('/main')

def main(request):
    return render(request, 'cars/main.html')

def display_cars(request, methods=['POST']):
    all_cars=[]
      
    if request.POST['make'] == 'AnyMake' :
        all_cars=Car.objects.filter(model__icontains=request.POST['model'],
                                    year__icontains= request.POST['year'])

    if request.POST['model'] == 'AnyModel':
        all_cars=Car.objects.filter(year__icontains=request.POST['year'],
                                    make__icontains=request.POST['make'])

    if request.POST['year'] == 'AnyYear' :
        all_cars=Car.objects.filter(make__icontains=request.POST['make'],
                                    model__icontains=request.POST['model'])

    if request.POST['year'] == 'AnyYear' and  request.POST['make'] == 'AnyMake' :
        all_cars=Car.objects.filter(model__icontains=request.POST['model'])  

    if request.POST['model'] == 'AnyModel' and request.POST['year'] == 'AnyYear':
        all_cars=Car.objects.filter(make__icontains=request.POST['make']) 

    if request.POST['make'] == 'AnyMake' and request.POST['model'] == 'AnyModel' :
        all_cars=Car.objects.filter(year__icontains= request.POST['year']) 

    if request.POST['make'] == 'AnyMake' and request.POST['model'] == 'AnyModel' and request.POST['year'] == 'AnyYear' :
        all_cars=Car.objects.all()
    if request.POST['make'] != 'AnyMake' and request.POST['model'] != 'AnyModel' and request.POST['year'] != 'AnyYear' :
        all_cars=Car.objects.filter(make__icontains=request.POST['make'],
                                    model__icontains=request.POST['model'],
                                    year__icontains= request.POST['year'])
    context={
        "all_cars": all_cars,
    }

    return render(request, 'cars/display_cars.html', context)

def show(request, id):
    context = {
		'car': Car.objects.get(id = id)
	}
    return render(request, 'cars/show.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def favorites(request,number):
    this_user = User.objects.get(id=request.session['id'])
    this_car = Car.objects.get(id = number)
    print("this_car", this_car.id)
    print("this_user", this_user.id)
    this_user.liked_cars.add(this_car)
    return render(request, 'cars/display_cars.html')

def remove_fav(request, id):
    context = {
        'cars': Car.objects.all(),
        'user': User.objects.get(id=request.session['id'])
    }
    this_user = User.objects.get(id=request.session['id'])
    this_car = Car.objects.get(id = id)
    this_user.liked_cars.remove(this_car)
    return redirect('/my_fav')

def my_fav(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': User.objects.get(id=request.session['id']),
        "my_fav": user.liked_cars.all()
    }
    print("request.session id: ", request.session['id'])
    return render(request, 'cars/my_fav.html', context)

def new_car(request):
    return render(request, 'cars/new_car.html')

def add_car(request):
    # errors = Job.objects.job_validator(request.POST)
    # if len(errors):
    #     for key, msg in errors.items():
    #         messages.error(request, msg, extra_tags=key)
    #     return redirect('/new_car')
    # else:
    car = Car.objects.create(
    make=request.POST['make_car'],
    model=request.POST['model'],
    year=request.POST['year'],
    price=request.POST['price'],
    pic=request.POST['pic'],
    desc=request.POST['car_desc'], 
    video=request.POST['video'],
    author_id = request.session['id']
    )
    messages.success(request, "Car successfully created")
    return redirect('/new_car')

def destroy_car(request, id):
    Car.objects.get(id=id).delete()
    print('Delete ', id)
    return redirect('/main')

def edit_car(request, id):
    context = {
		'car': Car.objects.get(id = id)
	}
    return render(request, 'cars/edit_car.html', context)

def update_car(request, id):
    if request.method == "POST":
        up_car = Car.objects.get(id = id) 
        up_car.make = request.POST['make_car']
        up_car.model = request.POST['model']
        up_car.year = request.POST['year']
        up_car.price = request.POST['price']
        up_car.pic = request.POST['pic']
        up_car.desc = request.POST['car_desc']
        up_car.video = request.POST['video']
        up_car.save()
        return redirect('/main')
