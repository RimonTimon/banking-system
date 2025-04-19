
from django import forms

from .models import Account , FixedDeposit

class AccountOpen(forms.ModelForm):
    class Meta:
        model = Account
        fields =  [
            'full_name', 'email', 'phone', 'date_of_birth', 'gender',
            'nationality', 'nid_passport', 'present_address', 'permanent_address',
            'account_type', 'balance', 'currency'
        ]
        
    
class DepositForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount ($)',
        min_value=1.00,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    source = forms.ChoiceField(
        label='From Account',
        choices=[
            ('cash', 'Cash'),
            ('external', 'External Account')
        ]
    )

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount ($)',
        min_value=1.00,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    method = forms.ChoiceField(
        label='Withdrawal Method',
        choices=[
            ('atm', 'ATM'),
            ('branch', 'Bank Branch')
        ]
    )

class TransferForm(forms.Form):
    amount = forms.DecimalField(
        label='Amount ($)',
        min_value=100.00,
        max_digits=9,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    recipient_account = forms.CharField(
        label='Recipient Account',
        max_length=20
    )
    note = forms.CharField(
        label='Note (Optional)',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Rent payment'})
    )
    
    

class FixedDepositForm(forms.ModelForm):
    class Meta:
        model = FixedDeposit
        fields = ['amount', 'tenure_months']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 1000:
            raise forms.ValidationError("Minimum FD amount is 1000.")
        return amount
    
    
