from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        null=True, 
        blank=True        
    )
    def __str__(self):
        return self.user.username


class TransactionCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=20, unique=True, editable=False)
    transaction_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('borrow', 'Borrow'),
        ('given', 'Given'),
    ]      
    
    category = models.ForeignKey('TransactionCategory', on_delete=models.SET_NULL, null=True, blank=True)   
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES, default='income')
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    description = RichTextField(null=True, blank=True)    
    invoice_no = models.CharField(max_length=15, null=True, blank=True)
    invoice_id = models.CharField(max_length=15, null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    check_no = models.CharField(max_length=15, null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            today_str = now().strftime('%m%d%Y')  # Format: MMDDYYYY
            last_transaction = Transaction.objects.filter(transaction_id__startswith=today_str).order_by('-transaction_id').first()
            
            if last_transaction:
                last_number = int(last_transaction.transaction_id[-4:])  # Get last 4 digits
                new_number = f"{last_number + 1:04d}"  # Increment and format with leading zeros
            else:
                new_number = "0001"

            self.transaction_id = f"{today_str}{new_number}"

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.transaction_by} - {self.transaction_type} - {self.price}"