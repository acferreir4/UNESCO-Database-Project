from django.db import models
from datetime import date

# Create your models here.
'''
class DynamicFormModel(models.Model):
    title
    type_ 

    data 
    #Have one char field as default
    active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        for idx, question in enumerate(kwargs['questions']):
            self.fields['Question {0}.'.format(idx + 1)] = models.TextField(help_text=question) 
'''

class DataTable(models.Model):
    form_id = models.ForeignKey('DynamicForms', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Questions', on_delete=models.CASCADE)
    #Change submitter_id back to use foreign key to user
    #submitter_id = models.ForeignKey('users.User', on_delete=models.PROTECT)
    submitter_id = models.CharField(max_length=100, blank=True, null=True)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)


class DynamicForms(models.Model):
    #Change creator_id back to user foreign key to user
    #creator_id = models.ForeignKey('users.User', on_delete=models.PROTECT)
    creator_id = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=300, unique=True)
    is_active = models.BooleanField(default=True)
    creation_time = models.DateTimeField(default=date.today)
    expiry_date = models.DateTimeField(default=date.today)

    class Meta:
        verbose_name_plural = "DynamicForms"

    def __str__(self):
        return self.title

class Questions(models.Model):
    form_id = models.ForeignKey('DynamicForms', on_delete=models.CASCADE)
    question_num = models.IntegerField()
    question_text = models.CharField(max_length=100000)
    answer_type = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_modification_time = models.DateTimeField(default=date.today)

    class Meta:
        verbose_name_plural = "Questions"
