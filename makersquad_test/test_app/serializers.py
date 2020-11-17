from rest_framework import serializers

from .models import Client, Invoice, InvoiceLine

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    last_invoice_date = serializers.DateField(source='get_last_invoice_date', read_only=True)
    vat_amount = serializers.FloatField(source='get_total_iva', read_only=True)
    total_amount = serializers.FloatField(source='get_total_price', read_only=True)
    number_of_invoices = serializers.IntegerField(source='get_number_of_invoices', read_only=True)

    class Meta:
        model = Client
        fields = ('name', 'last_invoice_date', 'vat_amount', 'total_amount', 'number_of_invoices')


# class InvoiceLineSerializer(serializers.HyperlinkedModelSerializer):
#     vat_amount = serializers.FloatField(source='get_total_iva', read_only=True)
#     total_amount = serializers.FloatField(source='get_total_price', read_only=True)
#     total_price_ht = serializers.FloatField(source='get_total_price_ht', read_only=True)
#     unit_price = serializers.FloatField(source='price_ht', read_only=True)
    
#     class Meta:
#         model = InvoiceLine
#         fields = ('title', 'quantity', 'unit_price', 'vat_amount', 'total_amount', 'total_price_ht')

class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    number_of_lines = serializers.IntegerField(source='get_number_of_lines', read_only=True)
    client_name = serializers.CharField(source='get_client_name', read_only=True)
    total_vat_amount = serializers.FloatField(source='get_total_iva', read_only=True)
    total_amount = serializers.FloatField(source='get_total_price', read_only=True)
    invoice_lines = serializers.ListField(source='get_all_lines_as_dict')
    
    class Meta:
        model = Invoice
        fields = ('client_name', 'number_of_lines', 'total_vat_amount', 'total_amount', 'invoice_lines')
