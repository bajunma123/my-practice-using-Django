from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Account

from .forms import LoginForm, UserEditForm, UserRegistrationForm

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None: 
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully') 
                else:
                    return HttpResponse('disable account')
        else:
            return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'templates/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_account = user_form.save(commit=False)
            # Set the chosen password
            new_account.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_account.save()
            # Create the user profile
            account = Account.objects.create(user=new_account)
            create_action(new_account, 'has created an account')
            return render(request,
                          'templates/register_done.html',
                          {'new_account': new_account})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'templates/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'edit.html', {'user_form': user_form})
