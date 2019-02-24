from django import forms

class DynamicQuestionForm(forms.Form):
    
    title = forms.CharField(max_length=300)

    def __init__(self, *args, **kwargs):
        self.question_nums = kwargs.pop('question_nums')
        super().__init__(*args, **kwargs)

        for i in range(self.question_nums):
            self.fields['Question {0}'.format(i + 1)] = forms.CharField(max_length=100000) 
