# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Quote, User
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "quotes/index.html")

def register(request):
    result = User.objects.validate_reg(request.POST)
    if result[0] == False:
        for error in result[1]:
            messages.error(request, error)
        return redirect("/")
    else:
        request.session['user_id'] = User.objects.get(email=request.POST['email']).id
        return redirect("/quotes")

def login(request):
    result = User.objects.validate_login(request.POST)
    if result[0] == False:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(email=request.POST['email']).id
        return redirect("/quotes")

def quotes(request):
    user = User.objects.get(id=request.session['user_id'])
    faves = user.faves.all()
    quotes = Quote.objects.exclude(favorites=request.session['user_id'])
    context = {
        'user': user,
        'faves': faves,
        'quotes': quotes
    }
    return render(request, "quotes/quotes.html", context)

def user_info(request, user_id):
    user = User.objects.get(id=user_id)
    my_quotes = user.quotes.all()
    context = {
        'user': user,
        'my_quotes': my_quotes
    }
    return render(request, "quotes/user_info.html", context)

def add_fave(request, quote_id):
    user = User.objects.get(id=request.session['user_id'])
    quote= Quote.objects.get(id=quote_id)
    user.faves.add(quote)
    return redirect("/quotes")

def remove_fave(request,quote_id):
    user = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.get(id=quote_id)
    user.faves.remove(quote)
    return redirect("/quotes")

def create(request):
    user_id = request.session['user_id']
    result = Quote.objects.validate_quote(request.POST, user_id)
    if result[0] == False:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/quotes')

def logout(request):
    del request.session['user_id']
    return redirect('/')