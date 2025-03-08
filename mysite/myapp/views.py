from django.shortcuts import render, redirect
from .models import Food, Consume
from django.contrib import messages
# Create your views here.


def index(request):
    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=consume)
        consume.save()
        foods = Food.objects.all()

    else:
        foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)

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
        food = Food(name=request.POST['inputFoodName'], calories=request.POST['inputCalories'], carbs=request.POST['inputCarbs'], protein=request.POST['inputProtein'], fats=request.POST['inputFats'])
        food.save()
        messages.success(request, f'🛒 {food.name} created successfully!')
        return render(request, 'myapp/createfood.html')
    else:
        return render(request, 'myapp/createfood.html')
