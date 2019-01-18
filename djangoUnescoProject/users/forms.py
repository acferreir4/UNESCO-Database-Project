from django import forms
from users.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    #Gives us nested namespace for configuration, keeps configs in one place
    #Within config, the model that will be affected is the User model 
    #(i.e. form.save() saves new field email into User model)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'role', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
