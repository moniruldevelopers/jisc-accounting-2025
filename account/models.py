from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # If User is deleted, Profile is deleted
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Not unique
    email = models.EmailField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class TransactionCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    transaction_by = models.ForeignKey(User, on_delete=models.CASCADE)
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('borrow', 'Borrow'),
        ('given', 'Given'),
    ]      
    category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True, blank=True)   
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES, default='income')
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    description = RichTextField(null=True, blank=True)    
    invoice_no = models.CharField(max_length=15, null=True, blank=True)
    invoice_id = models.CharField(max_length=15, null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    check_no = models.CharField(max_length=15, null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_by} - {self.transaction_type} - {self.price}"