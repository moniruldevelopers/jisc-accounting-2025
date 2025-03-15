from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('upload-users/', upload_users, name='upload_users'),
    path('', home, name='home'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('add-transaction/', add_edit_transaction, name='add_transaction'),  # Used for both Add/Edit
    path('transaction-print/<int:transaction_id>/', transaction_print, name='transaction_print'),
    path('edit-transaction/<int:transaction_id>/', add_edit_transaction, name='edit_transaction'),
    path('transactions/delete/<int:transaction_id>/', delete_transaction, name='delete_transaction'),



    # user related url
    path('users/', user_list, name='user_list'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/reset-password/<int:user_id>/', reset_password, name='reset_password'),


    # reports
    path('yearly-balance/', yearly_balance, name='yearly_balance'),
    path('yearly-given-borrow/', yearly_given_borrow, name='yearly_given_borrow'),   

    # category
    path('category-summary/', category_summary, name='category_summary'),
    path('category-transactions/<str:category_name>/', category_transactions, name='category_transactions'),


]
