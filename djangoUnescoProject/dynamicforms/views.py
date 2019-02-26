from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import DynamicQuestionForm
from .models import Forms, Questions, DataTable

# Create your views here.
def create_form(request):
    #questions = get_questions(request.POST)
    question_nums = 1

    if request.method == 'POST':        
        print(request.POST.get('numQuestions'))
            
        question_nums = int(request.POST.get('numQuestions')) + 1 if request.POST.get('numQuestions') else int(request.POST.get('save'))

    form = DynamicQuestionForm(request.POST if request.method == 'POST' else None, question_nums=question_nums)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        messages.success(request, f'The form {title} has been created, woohoo!')
        for key in form.cleaned_data.keys():
            if key != 'title':
                messages.success(request, f'The question {form.cleaned_data.get(key)} has been made, woohoo!')
        messages.success(request, f'The number of questions is: {question_nums}')

        '''Creating some forms:'''
        form = Forms.objects.create(
            name = title,
        )
        for key in form.cleaned_data.keys():
            if key != 'title':
                question = Questions.objects.create(
                    forms_id = form,
                    question_text = form.cleaned_data.get(key)

                )
        return redirect('register')

    return render (request, 'dynamicforms/create.html', {'form': form, 'numQuestions': question_nums})
    
