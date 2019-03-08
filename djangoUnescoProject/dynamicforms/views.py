from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import DynamicQuestionForm
from .models import DynamicForms, Questions, DataTable

# Create your views here.

def start_form(request):
    return render (request, 'dynamicforms/home.html', {'forms': DynamicForms.objects.all()})
    
def create_form(request):
    form_title = 'Create a New Form!'
    question_nums = 1
    form_questions = None
    title = None
    save = False
    is_answer = False
    if request.method == 'POST':
        form_questions = request.POST.dict()
        title = form_questions['title']
        if request.POST.get('save'):        
            question_nums = int(request.POST.get('save'))
            save = True
        else:
            if request.POST.get('add'):
                question_nums = int(request.POST.get('add')) + 1
            if request.POST.get('remove') and int(request.POST.get('remove')) > 1:
                question_nums = int(request.POST.get('remove')) - 1

    form = DynamicQuestionForm(request.POST if request.method == 'POST' and request.POST.get('save') else None, question_nums=question_nums, title=title, form_questions=form_questions, save=save, is_answer=is_answer)
    if form.is_valid():

        title = form.cleaned_data.get('title')
        messages.success(request, f'The form {title} has been created!')
        
        for key in form.cleaned_data.keys():
            if key != 'title':
                messages.success(request, f'The question {form.cleaned_data.get(key)} has been created!')
        messages.success(request, f'The number of questions is: {question_nums}')
        new_form = DynamicForms.objects.create(
            title = title,
        )
        counter = 1
        for key in form.cleaned_data.keys():
            if key != 'title':
                Questions.objects.create(
                    form_id = new_form,
                    question_num = counter,
                    question_text = form.cleaned_data.get(key),
                )
                counter += 1
        
        return redirect('form-home')
    context = {
        'form': form, 
        'numQuestions': question_nums, 
        'form_title': form_title,
    }
    return render (request, 'dynamicforms/form-create.html', context)

def form_edit(request, form_pk):
    if request.method == 'POST':
        if request.POST.get('delete'):
            to_delete_form = DynamicForms.objects.get(id=form_pk)
            title = to_delete_form.title
            to_delete_form.delete()
            messages.success(request, f'The form {title} has been successfully deleted!')

            return redirect('form-home')
    is_answer = False
    save = None
    title, questions, question_nums = __get_form_information(form_pk) 
    form_title = f'Editing Form {title}'
    form_questions = {}

    for question in questions:
        form_questions[f'Question {question.question_num}'] = question.question_text
    form = DynamicQuestionForm(request.POST if request.method == 'POST' and request.POST.get('save') else None, title=title, question_nums=question_nums, question_labels=None, form_questions=form_questions, save=save, is_answer=is_answer, form_pk=form_pk)
    context = {
        'form': form,
        'form_title': form_title,
        'form_pk': form_pk,
    }
    return render (request, 'dynamicforms/form-edit.html', context)
     

def form_answer(request, form_pk):
    is_answer = True
    save = None

    title, questions, question_nums = __get_form_information(form_pk)
    form_title = f'Answering Form {title}'

    question_labels = {}
    for question in questions:
        question_labels[question.question_num] = question.question_text
    form = DynamicQuestionForm(request.POST if request.method == 'POST' and request.POST.get('save') else None, title=title, question_nums=question_nums, question_labels=question_labels, form_questions=None, save=save, is_answer=is_answer)
    context = {
        'form': form,
        'form_title': form_title,
    }
    return render (request, 'dynamicforms/form-answer.html', context)

'''
    Database related functions that either manipulate or retrieve it
'''
def __get_form_information(form_pk):
    try:
        form_found = DynamicForms.objects.get(id=form_pk)        
        questions = Questions.objects.filter(form_id=form_pk)
        title = form_found.title
        question_nums = len(questions)

        return title, questions, question_nums
    except:
        return redirect('form-home') 
