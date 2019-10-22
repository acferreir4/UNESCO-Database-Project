from django.urls import path
from .views import (
        InstitutionDetailView, 
        InstitutionCreateView, 
        InstitutionUpdateView, 
        InstitutionDeleteView 
    )
from . import views

urlpatterns = [
    path('institution/export/csv', views.exportInstitutionsCsv, name='export-inst-csv'),
    path('institution/export/xlsx', views.exportInstitutionsXlsx, name='export-inst-xlsx'),
    path('institution/<int:pk>/', InstitutionDetailView.as_view(), name='institution-detail'),
    #path('institution/create/', InstitutionCreateView.as_view(), name='institution-create'),
    #path('institution/<int:pk>/update', InstitutionUpdateView.as_view(), name='institution-update'),
    #path('institution/<int:pk>/delete', InstitutionDeleteView.as_view(), name='institution-delete'),
]

# <app>/<model>_<viewtype>.html
