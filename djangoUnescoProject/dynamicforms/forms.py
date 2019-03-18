from django import forms
from .validator import validate_field, validate_title

class DynamicQuestionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        # The total number of questions in the form
        self.question_nums = kwargs.pop('question_nums')
        # Primary key of the form if creating the form from an existing model
        self.form_pk = None 
        if 'form_pk' in kwargs:
            self.form_pk = kwargs.pop('form_pk')
        # The actual questions of the form, created by an admin user
        self.form_questions = kwargs.pop('form_questions')
        # Check to validate the form input if saving the form
        self.save = True if 'save' not in kwargs else kwargs.pop('save')
        self.check_title = True if 'check_title' not in kwargs else kwargs.pop('check_title')
        self.title = kwargs.pop('title')
        # Variable used to check if the created form is meant for creating questions or answering them
        self.is_answer = kwargs.pop('is_answer')
        # Variable used to display the actual questions where answering a form
        self.question_labels = None if 'question_labels' not in kwargs else kwargs.pop('question_labels')
        # Variable used to grey out answers if form has been submitted
        self.is_submitted = False
        if 'is_submitted' in kwargs:
            if kwargs.pop('is_submitted'):
                self.is_submitted = True
        # Variable used to indicate if a draft of answers are being saved
        self.draft_or_display = False
        if 'draft_or_display' in kwargs:
            self.draft_or_display = kwargs.pop('draft_or_display')
        
        super().__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField(max_length=300,
                                               required=False,
                                               initial=self.title if self.title else '',
                                               disabled=self.is_answer)
        if not self.title:
            self.fields['title'].widget.attrs.update(autofocus='autofocus')
        # Put an error message for the title field if it is empty when trying to save the form
        if self.save and self.check_title:
            self.__validate_title_field()
        
        for i in range(self.question_nums):
            curr_key = f'Question {i + 1}'
            default_value = self.form_questions[curr_key] if self.form_questions and curr_key in self.form_questions else ''
            self.fields[curr_key] = forms.CharField(max_length=100000,
                                                    initial=default_value,
                                                    required=False,
                                                    label=f'Question {i+1}: {self.question_labels[i+1]}' if self.question_labels else None,
                                                    disabled=self.is_submitted)
            if len(default_value) == 0:
                self.fields[curr_key].widget.attrs.update(autofocus='autofocus')
            error_msg = validate_field(default_value)

            # Put an error message for all the fields that are not empty when trying to save the form
            if self.save and len(error_msg) > 0:
                # In the case of answering, only validate if submitting (not displaying or saving as draft)
                if not self.draft_or_display:
                    if self.form_questions and curr_key in self.form_questions:
                        self.errors[curr_key] = [error_msg]

    def __validate_title_field(self):
        error_msg = validate_field(self.title) or validate_title(self.title, self.form_pk)
        if len(error_msg) > 0:
            self.errors['title'] = [error_msg]
