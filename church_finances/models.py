from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User model

class Transaction(models.Model):
    """
    Model to represent a financial transaction (income or expense).
    """
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    # Common categories for church finances
    INCOME_CATEGORIES = (
        ('tithes', 'Tithes'),
        ('offerings', 'Offerings'),
        ('donations', 'Donations'),
        ('fundraising', 'Fundraising'),
        ('other_income', 'Other Income'),
    )

    EXPENSE_CATEGORIES = (
        ('salaries', 'Salaries'),
        ('utilities', 'Utilities'),
        ('rent_mortgage', 'Rent/Mortgage'),
        ('missions', 'Missions'),
        ('benevolence', 'Benevolence'),
        ('supplies', 'Supplies'),
        ('maintenance', 'Maintenance'),
        ('events', 'Events'),
        ('other_expense', 'Other Expense'),
    )

    date = models.DateField()
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=50,
                                choices=INCOME_CATEGORIES + EXPENSE_CATEGORIES,
                                help_text="Select a category for the transaction.")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at'] # Order by date descending, then creation time

    def __str__(self):
        return f"{self.date} - {self.get_type_display()}: {self.category} - ${self.amount}"

