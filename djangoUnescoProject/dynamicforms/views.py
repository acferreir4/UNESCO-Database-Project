from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import DynamicQuestionForm
from .models import DynamicForms, Questions, DataTable
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(redirect_field_name='login')
def start_form(request):
    return render (request, 'dynamicforms/home.html', {'forms': DynamicForms.objects.all()})

@login_required    
def create_form(request):
    if not request.user.is_staff:
        return redirect('form-home')
    form_title = 'Create a New Form!'
    question_nums = 1
    form_questions = None
    title = None
    is_answer = False
    save = False
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
        __create_form(request, form)
        return redirect('form-home')

    context = {
        'form': form, 
        'numQuestions': question_nums, 
        'form_title': form_title,
    }
    return render (request, 'dynamicforms/form-create.html', context)

@login_required
def form_edit(request, form_pk):
    if not request.user.is_staff:
        return redirect('form-home')
    
    is_answer = False
    if not form_pk and request.method == 'POST':
        form_pk = int(request.POST.get('update')) or int(request.POST.get('delete'))
    title, questions, question_nums = __get_form_information(request, form_pk) 
    original_title = title
    if not title and not questions and not question_nums:
        return redirect('form-home')
    form_title = f'Editing Form {title}'
    form_questions = {}

    if request.method == 'POST':
        if request.POST.get('delete'):
            try:
                to_delete_form = DynamicForms.objects.get(id=form_pk)
                to_delete_form.delete()
                messages.success(request, f'The form {title} has been successfully deleted!')
                return redirect('form-home')
            except:
                messages.error(request, 'An error occurred while trying to delete the form!')
                return redirect('form-home')
    if request.method == 'POST':
        form_questions = request.POST.dict() 
        title = form_questions['title']
    else:
        for question in questions:
            form_questions[f'Question {question.question_num}'] = question.question_text
    form = DynamicQuestionForm(request.POST if request.method == 'POST' and request.POST.get('update') else None, title=title, question_nums=question_nums, question_labels=None, form_questions=form_questions, is_answer=is_answer, form_pk=form_pk)
    if form.is_valid():
        try:
            # Title has changed, create a new form
            if original_title != title:
                __create_form(request, form)
            # Otherwise update all question fields
            else:
                counter = 1
                for key in form.cleaned_data.keys():
                    if key != 'title':
                        Questions.objects.filter(form_id=form_pk, question_num=counter).update(question_text=form.cleaned_data.get(key))
                        counter += 1
                messages.success(request, f'The form {title} was successfully updated!')
        except:
            messages.warning(request, 'An error occurred while trying to edit the form!')
        return redirect('form-home')
    context = {
        'form': form,
        'form_title': form_title,
        'form_pk': form_pk,
    }
    return render (request, 'dynamicforms/form-edit.html', context)
     
@login_required
def form_answer(request, form_pk):
    if request.user.is_staff:
        return redirect('form-home')
    is_answer = True
    check_title = False
    title, questions, question_nums = __get_form_information(request, form_pk) 
    if not title and not questions and not question_nums:
        return redirect('form-home')
    form_title = f'Answering Form {title}'

    question_labels = {}
    for question in questions:
        question_labels[question.question_num] = question.question_text
    form = DynamicQuestionForm(request.POST if request.method == 'POST' and request.POST.get('save') else None, title=title, question_nums=question_nums, question_labels=question_labels, form_questions=None, is_answer=is_answer, check_title=check_title)
    context = {
        'form': form,
        'form_title': form_title,
    }
    return render (request, 'dynamicforms/form-answer.html', context)

# Database related functions that either manipulate or retrieve it
def __get_form_information(request, form_pk):
    try:
        form_found = DynamicForms.objects.get(id=form_pk)        
        questions = Questions.objects.filter(form_id=form_pk)
        title = form_found.title
        question_nums = len(questions)

        return title, questions, question_nums
    except:
        messages.warning(request, 'An error occurred while trying to edit the form!')

        return None, None, None 

# Populates the database with the form fields 
def __create_form(request, form):
    try:
        title = form.cleaned_data.get('title')
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
        messages.success(request, f'The form {title} has been created!')    
    except:
        messages.error(request, 'An error occurred while trying to create the form!')