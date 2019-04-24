import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import DynamicQuestionForm
from .models import DynamicForms, Questions, DataTable
from django.contrib.auth.decorators import login_required
from users.models import User

# Create your views here.
@login_required(redirect_field_name='login')
def start_form(request):
    if not request.user.is_staff:
        # Create a mapping from form.id to status (complete, draft, new)
        form_status = {}
        user = User.objects.get(id=request.user.id)
        for form in DynamicForms.objects.all():
            dt_query = DataTable.objects.filter(form_id=form, submitter_id=user)
            # Get the first question and if answer exists, status determined by 'is_draft'
            # Otherwise if no answer exists, form is new
            question = Questions.objects.get(form_id=form, question_num=1)
            if dt_query.filter(question_id=question).exists():
                dt_obj = dt_query.get(question_id=question)
                if dt_obj.is_draft:
                    form_status[form] = "In Progress"
                else:
                    form_status[form] = "Complete"
            else:
                form_status[form] = "New"
        # We have to create a new 'forms' that makes this very unclean
        # Reason being django refuses to support a dictionary that uses a jinja2 variable as a key
        return render (request, 'dynamicforms/home.html', {'forms': form_status})
    if request.method == 'GET':
        if request.GET.get('download'):
            return export_form(request)
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

    # Build a context with all questions and saved draft answers
    context = __build_answer_context(request, form_pk)

    # The user presses either save button
    if request.method == 'POST':
        # Get the total # of questions in the form
        questions = [k for k in request.POST.keys() if "Question" in k]

        # Map all submitted answers with question ID
        answered_questions = {}
        for question in questions:
            answer = request.POST.get(question)
            question_id = question.split(' ')[-1]
            answered_questions[question_id] = answer

        # Write answers to DB
        if request.POST.get('save'):
            # Before saving, check to make sure all answers exist
            if __valid_answers(answered_questions):
                __save_final(form_pk, request.user.id, answered_questions)
                return redirect('form-home')
            else:
                context = __build_answer_context(request, form_pk)
                #messages.error(request,
                #               'All questions must be answered before submitting!')
        elif request.POST.get('temp_save'):
            __save_draft(form_pk, request.user.id, answered_questions)
            # Rebuild the context to show the saved answers in draft
            context = __build_answer_context(request, form_pk)
        else:
            messages.error(request, 'Something went wrong!')

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

"""Returns true if all answers given are valid (non-empty)"""
def __valid_answers(answered_questions):
    valid = False
    for _, answer in answered_questions.items():
        if not answer:
            valid = False
            break
        else:
            valid = True
    return valid

"""Save a user's draft of answers to the database
Parameters:
    [int] form_pk
    [int] user_id
    dict[int -> str] question_answer (question id to answer string)
"""
def __save_draft(form_pk, user_id, answered_questions):
    for question_id, answer in answered_questions.items():
        # Retrieve object from DB based on IDs for Foreign-key associations
        form = DynamicForms.objects.get(id=form_pk)
        question = Questions.objects.get(form_id=form_pk, question_num=question_id)
        user = User.objects.get(id=user_id)        
        # If an entry exists, update the answer. Otherwise, create a new entry
        if DataTable.objects.filter(form_id=form, question_id=question).exists():
            existing_entry = DataTable.objects.get(form_id=form, question_id=question)
            existing_entry.answer = answer
            existing_entry.save()
        elif answer:
            DataTable.objects.create(form_id=form, question_id=question,
                                     submitter_id=user, answer=answer, is_draft=True)

"""Save a user's answers to the database
Parameters:
    [int] form_pk
    [int] user_id
    dict[int -> str] question_answer (question id to answer string)
"""
def __save_final(form_pk, user_id, answered_questions):
    for question_id, answer in answered_questions.items():
        # Retrieve object from DB based on IDs for Foreign-key associations
        form = DynamicForms.objects.get(id=form_pk)
        question = Questions.objects.get(form_id=form_pk, question_num=question_id)
        user = User.objects.get(id=user_id)        
        # If an entry exists, update the answer. Otherwise, create a new entry
        if DataTable.objects.filter(form_id=form, question_id=question).exists():
            existing_entry = DataTable.objects.get(form_id=form, question_id=question)
            existing_entry.answer = answer
            existing_entry.is_draft = False
            existing_entry.save()
        else:
            DataTable.objects.create(form_id=form, question_id=question,
                                     submitter_id=user, answer=answer, is_draft=False)

"""Build a context with questions and saved draft answers for form-answer

Note that this function is called when showing the empty form for answering, and
for after answering the form. Thus, we must be careful when creating a
DynamicQuestionForm and be mindful of the current state in which we are creating it.
"""
def __build_answer_context(request, form_pk):
    is_answer = True
    check_title = False
    is_submitted = False
    title, questions, question_nums = __get_form_information(request, form_pk) 
    if not title and not questions and not question_nums:
        return redirect('form-home')
    form_title = f'Answering Form {title}'
    form_request = request.POST if request.method == 'POST' and request.POST.get('save') else None

    # Query the DataTable to find answers display them as default values.
    form = DynamicForms.objects.get(id=form_pk)
    user = User.objects.get(id=request.user.id)
    dt_query = DataTable.objects.filter(form_id=form, submitter_id=user)

    # form_questions is a dict of question_num -> answer
    form_questions = {}
    question_labels = {}

    # Indicate if user is saving answers as draft
    draft_or_display = False if request.POST.get('save') else True
    # Indicate if user is saving answers
    save = False

    for question in questions:
        question_labels[question.question_num] = question.question_text
        if dt_query.filter(question_id=question).exists():
            save = True
            dt_obj = dt_query.get(question_id=question)
            answer = dt_obj.answer
            is_submitted = not dt_obj.is_draft
            form_questions[f'Question {question.question_num}'] = answer
        else:
            form_questions[f'Question {question.question_num}'] = ""

    form = DynamicQuestionForm(form_request, title=title, question_nums=question_nums,
                               question_labels=question_labels,
                               form_questions=form_questions, is_answer=is_answer,
                               check_title=check_title, is_submitted=is_submitted,
                               save=save, draft_or_display=draft_or_display)
    context = {
        'form': form,
        'form_title': form_title,
        'hide_buttons': is_submitted,
    }
    
    return context

def export_form(request):
    """Return a CSV file of USERNAME, Q1, Q2, ... QN for all users that answered the
    form"""
    # Get the form object from id
    form = DynamicForms.objects.get(id=request.GET.get('download'))

    # Prepare the HttpResponse object
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(form.title)
    writer = csv.writer(response)

    # Construct CSV columns with username and questions in form
    csv_columns = ['Username', 'Institution',]
    questions = Questions.objects.filter(form_id=form)
    for question in questions:
        csv_columns.append(question.question_text)
    writer.writerow(csv_columns)
    
    # Populate CSV with columns of all users who answered form & their answers
    # If a user answered a question and it's not a draft, then it can be assumed that
    # they answered the whole form
    respondents = DataTable.objects.filter(form_id=form, question_id=question,
                                           is_draft=False)
    # For each person who answered the form
    for respondent in respondents:
        # Get their username
        user = respondent.submitter_id
        username = user.username
        institution = user.institution.name
        csv_row = [username, institution]
        # Get all their answers
        answers = DataTable.objects.filter(submitter_id=user, form_id=form)
        for answer in answers:
            csv_row.append(answer.answer)
        # Write the row
        writer.writerow(csv_row)

    return response
