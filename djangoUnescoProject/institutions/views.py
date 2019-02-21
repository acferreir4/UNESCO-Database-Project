from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import InstitutionCreateForm
from .models import Institution

# Create your views here.
def createInstitution(request):
    if request.method == 'POST':
        form = InstitutionCreateForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'Institution %s has been created!' % name)
            return redirect('createInstitution')
    else:
        form = InstitutionCreateForm()
    return render(request, 'institutions/create_institution.html', {'form':form})

def institutionProfile(request):
    return render(request, 'institutions/institution_profile.html')

def manageInstitutions(request):
    context = {
        'institutions': Institution.objects.all()
    }
    return render(request, 'institutions/manage_institution.html', context)

