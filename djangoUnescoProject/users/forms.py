from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    #Gives us nested namespace for configuration, keeps configs in one place
    #Within config, the model that will be affected is the User model 
    #(i.e. form.save() saves new field email into User model)
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'institution', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'role', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
