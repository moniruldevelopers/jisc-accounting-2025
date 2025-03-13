import pandas as pd
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models import Sum
from datetime import date
from django.utils.timezone import now
from .models import Transaction
from datetime import datetime
from django.utils.timezone import localtime
import pytz



def upload_users(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            new_users_count = 0
            existing_users_count = 0

            try:
                df = pd.read_excel(file)

                for index, row in df.iterrows():
                    username = str(row['id']).strip()
                    full_name = row['full name'].strip()
                    phone_number = str(row['phone number']).strip() if 'phone number' in row and pd.notna(row['phone number']) else None
                    password = username  # Default password = username

                    # Create or get the User
                    user, created = User.objects.get_or_create(
                        username=username,
                        defaults={'first_name': full_name}
                    )

                    if created:
                        user.set_password(password)
                        user.save()
                        new_users_count += 1
                    else:
                        existing_users_count += 1

                    # Manually create the Profile if it doesn't exist
                    profile, created = Profile.objects.get_or_create(user=user)

                    # Update the phone number if available
                    if phone_number:
                        profile.phone_number = phone_number
                        profile.save()

                messages.success(request, f'Upload completed! {new_users_count} new users added, {existing_users_count} users already existed.')
            except Exception as e:
                messages.error(request, f'Error processing file: {e}')

            return redirect('upload_users')
    else:
        form = UploadExcelForm()

    return render(request, 'user/upload_users.html', {'form': form})


def home(request):
    # Get Bangladesh timezone
    bd_timezone = pytz.timezone("Asia/Dhaka")
    
    # Get the selected date from the request (or use today's date as default)
    filter_date_str = request.GET.get('filter_date')
    
    # If a filter date is provided, convert it to a datetime object
    if filter_date_str:
        filter_date = datetime.strptime(filter_date_str, "%Y-%m-%d").date()
    else:
        # Default to today's date
        filter_date = localtime().date()

    # Format the selected date for displaying in the template
    formatted_date = filter_date.strftime("%d %B, %Y")
    
    # Filter transactions by the selected date
    transactions = Transaction.objects.filter(created_date__date=filter_date)

    # Calculate totals for income, borrow, expense, and given
    total_income = sum(t.price for t in transactions if t.transaction_type == 'income')
    total_borrow = sum(t.price for t in transactions if t.transaction_type == 'borrow')
    total_expense = sum(t.price for t in transactions if t.transaction_type == 'expense')
    total_given = sum(t.price for t in transactions if t.transaction_type == 'given')

    # Calculate the available balance
    available_balance = (total_income + total_borrow) - (total_expense + total_given)

    # Pass the required context to the template
    context = {
        'transactions': transactions,
        'selected_date': filter_date.strftime("%Y-%m-%d"),  # For the input field in the filter
        'formatted_date': formatted_date,  # For displaying "14 March, 2025"
        'total_income': total_income,
        'total_borrow': total_borrow,
        'total_expense': total_expense,
        'total_given': total_given,
        'available_balance': available_balance,
    }
    return render(request, 'home.html', context)




def add_edit_transaction(request, transaction_id=None):
    transaction = None

    if transaction_id:
        transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            # Save the transaction
            saved_transaction = form.save()

            # Get the user's full name from the transaction
            user_full_name = saved_transaction.transaction_by.get_full_name() or saved_transaction.transaction_by.username

            # Display success message with the user's full name
            messages.success(request, f"Transaction added successfully for {user_full_name}!")

            return redirect('transaction_list')
            
    else:
        form = TransactionForm(instance=transaction)

    # Override the transaction_by field to show "username - full name"
    form.fields['transaction_by'].queryset = User.objects.all()
    form.fields['transaction_by'].label_from_instance = lambda obj: f"{obj.username} - {obj.get_full_name() or obj.username}"

    return render(request, 'transactions/add_transaction.html', {'form': form, 'transaction': transaction})

def transaction_list(request):
    search_query = request.GET.get('search', '')

    # Create a base queryset, ordering by latest first
    transactions = Transaction.objects.all().order_by('-id')  # Sorting by latest first

    # Apply search filter if search query is present
    if search_query:
        transactions = transactions.filter(
            Q(transaction_by__username__icontains=search_query) |
            Q(transaction_by__first_name__icontains=search_query) |
            Q(transaction_by__last_name__icontains=search_query) |
            Q(price__icontains=search_query) |
            Q(invoice_id__icontains=search_query) |
            Q(check_no__icontains=search_query) |
            Q(transaction_by__profile__phone_number__icontains=search_query)  # Search by phone number
        )

        if transactions.exists():
            messages.success(request, f"Found {transactions.count()} matching transaction(s).")
        else:
            messages.warning(request, "No matching transactions found.")

    # Pagination: Show 10 transactions per page
    paginator = Paginator(transactions, 2)  # Show 10 transactions per page
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)

    context = {
        'transactions': transactions,
        'search_query': search_query,
    }

    return render(request, 'transactions/transaction_list.html', context)


def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    # Get the full name of the user who created the transaction
    user_full_name = transaction.transaction_by.get_full_name() or transaction.transaction_by.username

    # Delete the transaction
    transaction.delete()

    # Add the success message with the user's full name
    messages.success(request, f"Transaction deleted successfully for {user_full_name}.")

    # Redirect to the transaction list page
    return redirect('transaction_list')