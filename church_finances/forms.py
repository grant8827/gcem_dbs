from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction

class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form to extend Django's default.
    You can add more fields here if needed in the future.
    """
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",) # Add email field to registration

class TransactionForm(forms.ModelForm):
    """
    Form for creating and updating financial transactions.
    """
    # Override category field to dynamically show choices based on type if needed
    # For simplicity, we combine all categories here.
    # In a more complex app, you might use JavaScript to filter categories based on type selection.
    
    class Meta:
        model = Transaction
        fields = ['date', 'type', 'category', 'amount', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input rounded-md shadow-sm'}),
            'type': forms.Select(attrs={'class': 'form-select rounded-md shadow-sm'}),
            'category': forms.Select(attrs={'class': 'form-select rounded-md shadow-sm'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input rounded-md shadow-sm', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea rounded-md shadow-sm'}),
        }
        labels = {
            'date': 'Date',
            'type': 'Transaction Type',
            'category': 'Category',
            'amount': 'Amount ($)',
            'description': 'Description (Optional)',
        }
