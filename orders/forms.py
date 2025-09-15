from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'address', 'note']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Ismingizni kiriting'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Telefon raqamingiz'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Manzilingiz'
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'rows': 3,
                'placeholder': 'Qo‘shimcha izoh (ixtiyoriy)'
            }),
        }
        labels = {
            'customer_name': 'Ism Familiya',
            'phone': 'Telefon raqami',
            'address': 'Manzil',
            'note': 'Izoh',
        }
