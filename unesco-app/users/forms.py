from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = PhoneNumberField(
            error_messages={'require': 'Enter a valid phone number. Format: +1234567890'}
            )
    password1 = None
    password2 = None

    #Gives us nested namespace for configuration, keeps configs in one place
    #Within config, the model that will be affected is the User model 
    #(i.e. form.save() saves new field email into User model)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'role', 'institution']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    phone_number = PhoneNumberField(
            error_messages={'require': 'Enter a valid phone number. Format: +1234567890'}
            )

    class Meta:
        model = User
        fields = ['email', 'phone_number']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []
