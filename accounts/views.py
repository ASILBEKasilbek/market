from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomRegisterForm

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = CustomRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
