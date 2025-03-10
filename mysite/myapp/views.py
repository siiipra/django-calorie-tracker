from django.shortcuts import render, redirect
from .models import Food, Consume
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import datetime
# Create your views here.


def index(request):
    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        quantity = request.POST['quantity']
        date_consumed = request.POST['date']
        food = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=food, quantity=quantity, date_consumed=date_consumed)
        consume.save()
        foods = Food.objects.all()
    else:
        foods = Food.objects.all()
    consumed_food = []
    if request.user.is_authenticated:
        if 'startdate' in request.GET and 'enddate' in request.GET:
            startdate=request.GET['startdate']
            enddate=request.GET['enddate']
            consumed_food = Consume.objects.filter(user=request.user,date_consumed__range=(startdate, enddate))
        else:
            consumed_food = Consume.objects.filter(user=request.user,date_consumed=datetime.date.today())

    return render(request, 'myapp/index.html', {'foods': foods, 'consumed_food': consumed_food})


def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'myapp/delete.html')


def create_food(request):
    if request.method == 'POST':
        print(request.POST['inputFoodName'])
        food = Food(name=request.POST['inputFoodName'], calories=request.POST['inputCalories'],
                    carbs=request.POST['inputCarbs'], protein=request.POST['inputProtein'],
                    fats=request.POST['inputFats'])
        food.save()
        messages.success(request, f'🛒 {food.name} created successfully!')
        return render(request, 'myapp/createfood.html')
    else:
        return render(request, 'myapp/createfood.html')


def signup(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['inputUserName'], password=request.POST['inputPassword'])
        messages.success(request, f'🛒 New user {user.username} created successfully!')
    return render(request, 'myapp/signup.html')


def log_in(request):
    if request.method == 'POST':
        username = request.POST["inputUserName"]
        password = request.POST["inputPassword"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, f' Invalid user name or password!')
    return render(request, 'myapp/login.html')


def log_out(request):
    logout(request)
    return redirect('index')


