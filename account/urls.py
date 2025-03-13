from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('upload-users/', upload_users, name='upload_users'),
    path('', home, name='home'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('add-transaction/', add_edit_transaction, name='add_transaction'),  # Used for both Add/Edit
    path('edit-transaction/<int:transaction_id>/', add_edit_transaction, name='edit_transaction'),
    path('transactions/delete/<int:transaction_id>/', delete_transaction, name='delete_transaction'),

]
