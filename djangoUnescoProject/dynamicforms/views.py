from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import DynamicQuestionForm
from .models import Forms, Questions, DataTable

# Create your views here.

def start_form(request):
    return render (request, 'dynamicforms/home.html')
    
def create_form(request):
    #questions = get_questions(request.POST)
    question_nums = 1
    form_questions = None
    save = False
    if request.method == 'POST':
        form_questions = request.POST.dict()

        if request.POST.get('save'):        
        #question_nums = int(request.POST.get('numQuestions')) + 1 if request.POST.get('add') else int(request.POST.get('save'))
            question_nums = int(request.POST.get('save'))
            save = True
        else:
            if request.POST.get('add'):
                question_nums = int(request.POST.get('add')) + 1
            if request.POST.get('remove') and int(request.POST.get('remove')) > 1:
                question_nums = int(request.POST.get('remove')) - 1

    form = DynamicQuestionForm(request.POST if request.method == 'POST' and request.POST.get('save') else None, question_nums=question_nums, form_questions=form_questions, save=save)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        messages.success(request, f'The form {title} has been created!')
        
        for key in form.cleaned_data.keys():
            if key != 'title':
                messages.success(request, f'The question {form.cleaned_data.get(key)} has been created!')
        messages.success(request, f'The number of questions is: {question_nums}')

        '''Creating some forms:
        form = Forms.objects.create(
            name = title,
        )
        for key in form.cleaned_data.keys():
            if key != 'title':
                question = Questions.objects.create(
                    forms_id = form,
                    question_text = form.cleaned_data.get(key),
                )
        '''
        
        return redirect('register')
    return render (request, 'dynamicforms/create.html', {'form': form, 'numQuestions': question_nums})
    