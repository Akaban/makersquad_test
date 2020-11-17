from django import forms

from .models import Client, InvoiceLine, Invoice

class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name',)

class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ('client',)

