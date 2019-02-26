import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import User

def register(request):
    if not request.user.is_staff:
        return redirect('access-denied')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account for user %s has been created!' % username)
            return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
            'u_form': u_form,
            'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def accessDenied(request):
    return render(request, 'users/access_denied.html')


def exportUsers(request):
    if not request.user.is_staff:
        return redirect('access-denied')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Username', 
        'First Name', 
        'Last Name', 
        'Email',
        'Institution',
        'Role',
        'Admin',
        'Active',
        'Date Registered',
        'Last Login',
        ])

    for user in User.objects.order_by('institution'):
        writer.writerow([
            user.username, 
            user.first_name, 
            user.last_name, 
            user.email,
            user.institution,
            user.role,
            'Yes' if user.is_staff else 'No',
            'Yes' if user.is_active else 'No',
            user.date_joined,
            user.last_login,
            ])

    return response
