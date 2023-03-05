from django.urls import path
from .views import *

app_name = 'application'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('help/', help_view, name='help'),
    path('accounts/login/', view_login, name='login'),
    path('accounts/logout/', view_logout, name='logout'),

    path('employees/', employees, name='employees'),
    path('employee/<int:pk>/', employee, name='employee'),
    path('add/employee/', add_employee, name='add_employee'),
    path('update/employee/<int:pk>/', update_employee, name='update_employee'),
    path('delete/employee/<int:pk>/', delete_employee, name='delete_employee'),

    path('reviews/', reviews, name='reviews'),
    path('review/<int:pk>/', review, name='review'),
    path('add/review/', add_review, name='add_review'),
    path('update/review/<int:pk>/', update_review, name='update_review'),
    path('delete/review/<int:pk>/', delete_review, name='delete_review'),

    path('emp_reviews', emp_reviews, name='emp_reviews'),
]
