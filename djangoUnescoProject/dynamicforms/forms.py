from django import forms
from .validators import validator

class DynamicQuestionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.question_nums = kwargs.pop('question_nums')
        self.form_questions = kwargs.pop('form_questions')
        self.save = kwargs.pop('save')
        super().__init__(*args, **kwargs)
        self.fields['title'] = forms.CharField(max_length=300, required=False, initial=self.form_questions['title'] if self.form_questions else '')
        
        # Put an error message for the title field if it is empty when trying to save the form
        if self.save:
            error_msg = validator.validate_field(self.form_questions['title'])
            if len(error_msg) > 0:
                self.errors['title'] = [error_msg]

        for i in range(self.question_nums):
            default_value = self.form_questions['Question {0}'.format(i + 1)] if self.form_questions and 'Question {0}'.format(i + 1) in self.form_questions else ''
            self.fields['Question {0}'.format(i + 1)] = forms.CharField(max_length=100000, initial=default_value, required=False)
            error_msg = validator.validate_field(default_value)
            
            # Put an error message for all the fields that are not empty when trying to save the form
            if self.save and len(error_msg) > 0:
                print(error_msg, default_value)
                if self.form_questions and 'Question {0}'.format(i + 1) in self.form_questions:
                    self.errors['Question {0}'.format(i + 1)] = [error_msg]
   