from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from orders.models import Order
from .forms import RegistrationForm, UserEditForm
from .models import UserBase

# Create your views here.


@login_required
def dashboard(request):
    """
    Shows the dashboard for logged users.
    """
    orders = Order.objects.all().filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request,
                  'account/user/dashboard.html', context=context)


def account_register(request):
    """
    Allows to create new users.
    """
    if request.user.is_authenticated:
        return redirect('/shop/')

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.first_name = registerForm.cleaned_data['first_name']
            user.last_name = registerForm.cleaned_data['last_name']
            user.is_active = True
            user.save()
            user = UserBase.objects.get(pk=user.pk)
            if user is not None:
                login(request, user)
            message = 'Twoje konto zostało poprawnie utworzone.'
            context = {
                'message': message
            }
            return render(request, 'account/user/dashboard.html', context=context)

    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


@login_required
def edit_details(request):
    """
    Allows edit the contact's details.
    """
    if request.method == 'POST':
        form = UserEditForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            message = "Dane zostały pomyślnie zapisane"
            return render(request, 'account/user/dashboard.html', {'message': message})
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'account/user/edit_details.html', {'form': form})
@login_required
def delete_user(request):
    """
    Allows to deactivate account.
    """
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

