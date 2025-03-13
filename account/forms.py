from django import forms
from .models import Transaction
from ckeditor.widgets import CKEditorWidget
from django.forms.widgets import DateInput

class UploadExcelForm(forms.Form):
    file = forms.FileField()


class TransactionForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = Transaction
        fields = ['transaction_by', 'category', 'transaction_type', 'price', 
                  'invoice_no', 'invoice_id', 'invoice_date', 'check_no', 'description']
        widgets = {
            'transaction_by': forms.Select(attrs={'class': 'form-control select2'}),
            'category': forms.Select(attrs={'class': 'form-control select2'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
            'invoice_id': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_no': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '15'}),
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price