from django.http import request
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import*

# Create your views here.
def index(request):
    return redirect("/mainpage")

def mainpage(request):
    return render(request, "index.html")

def register(request):
    print(request.POST)
    validationErrors = User.objects.reg_validator(request.POST)
    if len(validationErrors) > 0:
        for key, value in validationErrors.items():
            messages.error(request, value, extra_tags= "reg")
        return redirect("/mainpage")
    
    newUser = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = request.POST['pw'])
    request.session['loggedInId'] = newUser.id    
    return redirect("/travels")

def login(request):
    print(request.POST)
    ValidationErrors = User.objects.login_validator(request.POST)
    if len(ValidationErrors) > 0:
        for key, value in ValidationErrors.items():
            messages.error(request, value, extra_tags="login")
        return redirect("/mainpage")
    filteredResult = User.objects.filter(username = request.POST["usrnm"])
    request.session['loggedInId'] = filteredResult[0].id
    return redirect("/travels")

def travels(request):
    if 'loggedInId' not in request.session:
        return redirect("/mainpage")
    
    loggedInUser = User.objects.get(id = request.session['loggedInId'])
    context = {
        "allTravel": Travel.objects.all(),
        "allUsers": User.objects.all(),
        "loggedInUser": loggedInUser,
        "favitems": Travel.objects.filter(favorites = User.objects.get(id = request.session['loggedInId'])),
        "nonfavitems": Travel.objects.exclude(favorites = User.objects.get(id = request.session['loggedInId']))
    }
    return render(request, "travels.html", context)

def logout(request):
    request.session.clear()
    return redirect("/mainpage")

def addTravel(request):
    return render(request, "create.html")

def add(request):
    validationErrors = Travel.objects.itemValidator(request.POST)
    loggedInUser = User.objects.get(id = request.session['loggedInId'])

    if len(validationErrors) > 0:
        for key, value in validationErrors.items():
            messages.error(request, value, extra_tags="login")
        return redirect("/travels/add")
    newItem = Travel.objects.create(destination = request.POST['destin'], plan = request.POST['descrip'], travel_start = request.POST['from'], travel_end = request.POST['to'], uploader = loggedInUser)

    loggedInUser.travelFav.add(newItem)
    return redirect("/travels")

def destination(request, favId):
    print(Travel.objects.get(id=favId))

    context = {
        'favUser': Travel.objects.get(id=favId).favorites.all(),
        'selectedItem': Travel.objects.get(id = favId),
        "allUsers": User.objects.all(),
    }
    return render(request, "destination.html", context)

def favoriteItem(request, favId):
    itemTofav = Travel.objects.get(id=favId)
    loggedinuser = User.objects.get(id = request.session['loggedInId'])
    itemTofav.favorites.add(loggedinuser)
    return redirect("/travels")
