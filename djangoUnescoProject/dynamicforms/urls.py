from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_form, name="form-home"),
    path('create-forms/', views.create_form, name="create-form")
]

# <app>/<model>_<viewtype>.html
