from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_form, name='form-home'),
    path('form-create/', views.create_form, name='form-create'),
    path('form-edit/<int:form_pk>', views.form_edit, name='form-edit'),
    path('form-answer/<int:form_pk>', views.form_answer, name='form-answer'),
]

# <app>/<model>_<viewtype>.html
