from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.

def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
    context = {
        'form':form,
    }  
    return render(request, 'registration/register.html', context)      

