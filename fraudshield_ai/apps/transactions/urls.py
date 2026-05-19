from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('check/', views.transaction_check, name='check'),
    path('history/', views.transaction_history, name='history'),
]
