from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.messages import success, error, info
from django.db.models import Sum
from .models import Transaction
from .forms import CustomUserCreationForm, TransactionForm
from django.contrib.auth.forms import AuthenticationForm # For login form

def register_view(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in immediately after registration
            success(request, 'Registration successful! You are now logged in.')
            return redirect('dashboard')
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'church_finances/register.html', {'form': form})

def user_login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'church_finances/login.html', {'form': form})

@login_required
def user_logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def dashboard_view(request):
    """
    Displays a financial summary dashboard.
    """
    total_income = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expense

    recent_transactions = Transaction.objects.all()[:10] # Display last 10 transactions

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'church_finances/dashboard.html', context)

@login_required
def transaction_list_view(request):
    """
    Displays a list of all financial transactions.
    """
    transactions = Transaction.objects.all()
    context = {'transactions': transactions}
    return render(request, 'church_finances/transaction_list.html', context)

@login_required
def transaction_create_view(request):
    """
    Handles creation of new financial transactions.
    """
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.recorded_by = request.user # Assign the current user as recorder
            transaction.save()
            success(request, 'Transaction added successfully!')
            return redirect('transaction_list')
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = TransactionForm()
    return render(request, 'church_finances/transaction_form.html', {'form': form, 'title': 'Add New Transaction'})

@login_required
def transaction_detail_view(request, pk):
    """
    Displays details of a single transaction.
    """
    transaction = get_object_or_404(Transaction, pk=pk)
    context = {'transaction': transaction}
    return render(request, 'church_finances/transaction_detail.html', context)

@login_required
def transaction_update_view(request, pk):
    """
    Handles updating an existing financial transaction.
    """
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            success(request, 'Transaction updated successfully!')
            return redirect('transaction_detail', pk=pk)
        else:
            for field, errors_list in form.errors.items():
                for err in errors_list:
                    error(request, f"{field}: {err}")
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'church_finances/transaction_form.html', {'form': form, 'title': 'Update Transaction'})

@login_required
def transaction_delete_view(request, pk):
    """
    Handles deletion of a financial transaction.
    """
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        success(request, 'Transaction deleted successfully!')
        return redirect('transaction_list')
    return render(request, 'church_finances/confirm_delete.html', {'transaction': transaction})
