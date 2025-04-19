from django.shortcuts import render ,redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AccountOpen
from .models import Account ,Transaction , FixedDeposit
from django.contrib import messages
from .forms import DepositForm, WithdrawForm, TransferForm , FixedDepositForm
from decimal import Decimal

def landing_page(request):
    account = None
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user = request.user)
        except Account.DoesNotExist:
            account = None
            
    return render(request, 'landing_page.html', {'account':account})

@login_required
def dashboard(request):
    woner = get_object_or_404(Account , user = request.user)
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-timestamp')[:4]
    context = {
        "transactions":transactions,
        "woner":woner
    }
    return render(request, 'dashboard.html', context)

@login_required
def transactions(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-timestamp')
    return render(request, 'transaction.html', {'transactions': transactions})

@login_required
def account(request):
    if request.method == "POST":
        form = AccountOpen(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            form.save()
            return redirect('dashboard')
        
    else:
        form = AccountOpen()
        
    return render(request, 'account.html', {"form":form})



@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            # Process deposit
            amount = form.cleaned_data['amount']
            account = request.user.account
            account.balance += amount
            account.save()
            
            # Create transaction record
            Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type='deposit',
                description=f"Deposit from {form.cleaned_data['source']}"
            )
            return redirect('dashboard')
    else:
        form = DepositForm()
    
    return render(request, 'deposit.html', {'form': form})

@login_required
def withdraw(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = request.user.account
            
            # Check sufficient balance
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='withdrawal',
                    description=f"Withdrawal via {form.cleaned_data['method']}"
                )
                return redirect('dashboard')
            else:
                form.add_error('amount', 'Insufficient funds')
    else:
        form = WithdrawForm()
    
    return render(request, 'withdraw.html', {'form': form})

@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_account_number = form.cleaned_data['recipient_account']
            account = request.user.account
            
            try:
                recipient = Account.objects.get(account_number=recipient_account_number)
                
                if account.balance >= amount:
                    # Deduct from sender
                    account.balance -= amount
                    account.save()
                    
                    # Add to recipient
                    recipient.balance += amount
                    recipient.save()
                    
                    # Create transactions
                    Transaction.objects.create(
                        account=account,
                        amount=-amount,
                        transaction_type='transfer',
                        description=f"Transfer to {recipient_account_number}"
                    )
                    
                    Transaction.objects.create(
                        account=recipient,
                        amount=amount,
                        transaction_type='transfer',
                        description=f"Transfer from {account.account_number}"
                    )
                    return redirect('dashboard')
                else:
                    form.add_error('amount', 'Insufficient funds')
            except Account.DoesNotExist:
                form.add_error('recipient_account', 'Account not found')
    else:
        form = TransferForm()
    
    return render(request, 'transfer.html', {'form': form})


def create_fd(request):
    if request.method == 'POST':
        form = FixedDepositForm(request.POST)
        if form.is_valid():
            fd = form.save(commit=False)
            fd.user = request.user
            fd.interest_rate = 7.5

            interest = (fd.amount * Decimal(fd.interest_rate) * fd.tenure_months) / Decimal(1200)
            fd.maturity_amount = fd.amount + interest
            fd.save()
            
            messages.success(request, 'fd done')
            return redirect('dashboard')
    else:
        form = FixedDepositForm()
    return render(request, 'fd.html', {'form': form})


@login_required
def fd_account_view(request):
    fds = FixedDeposit.objects.filter(user=request.user)

    total_balance = sum(fd.amount for fd in fds if fd.amount is not None)
    total_maturity = sum(fd.maturity_amount for fd in fds if fd.maturity_amount is not None)

    context = {
        'fds': fds,
        'total_balance': total_balance,
        'total_maturity': total_maturity,
    }

    return render(request, 'fd_view.html', context)