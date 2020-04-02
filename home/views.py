from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django import forms
import os 

#commande pour upload
#echo -e "open 127.0.0.1 8888 \nuser user 12345 \nput upload.bmp uploaded.bmp\nbye" |ftp -n
def index(request):
    template = loader.get_template('home/index.html')
    context = {'titre' : "Coucou Hélo"}
    
    return render(request, 'home/index.html', context)      