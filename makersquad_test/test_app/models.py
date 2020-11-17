import datetime

from django.db import models

# Create your models here.

class Client(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def get_all_invoices(self):
        invoices = Invoice.objects.all().filter(client_id=self.id)
        return invoices

    @property
    def get_number_of_invoices(self):
        return len(self.get_all_invoices)

    @property
    def get_total_iva(self):
        total_iva = sum(
            map(lambda i: i.get_total_iva, self.get_all_invoices)
        )
        return total_iva
    
    @property
    def get_total_price_ht(self):
        total_price_ht = sum(
            map(lambda i: i.get_total_price_ht, self.get_all_invoices)
        )
        return total_price_ht
    
    @property
    def get_total_price(self):
        total_price = sum(
            map(lambda i: i.get_total_price, self.get_all_invoices)
        )
        return total_price

    @property
    def get_last_invoice(self):
        invoices = self.get_all_invoices

        if len(invoices) == 0:
            raise ValueError("Cannot return the last invoice of client since there is no associated invoices")

        return invoices.latest("invoice_date")

    @property
    def get_last_invoice_date(self):
        if self.get_number_of_invoices == 0:
            return None
        else:
            return self.get_last_invoice.invoice_date

class Invoice(models.Model):

    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    # il n'est normalement pas nécessaire de créer ce champ car le champ id de django
    # se comporte déjà de manière auto incrémentale par défaut
    # dans le contexte de ce test on le crée quand même et on le définit comme primary key
    invoice_id = models.AutoField(primary_key=True)

    invoice_date = models.DateField(default=datetime.date.today)

    @property
    def get_all_invoice_lines(self):
        lines = InvoiceLine.objects.all().filter(invoice_id=self.invoice_id)
        return lines

    @property
    def get_number_of_lines(self):
        return len(self.get_all_invoice_lines)

    @property
    def get_total_iva(self):
        total_iva = sum(
            map(lambda l: l.get_total_iva, self.get_all_invoice_lines)
        )
        return total_iva
    
    @property
    def get_total_price_ht(self):
        total_price_ht = sum(
            map(lambda l: l.get_total_price_ht, self.get_all_invoice_lines)
        )
        return total_price_ht
    
    @property
    def get_total_price(self):
        total_price = sum(
            map(lambda l: l.get_total_price, self.get_all_invoice_lines)
        )
        return total_price

    @property
    def get_client_name(self):
        return self.client.name

    @property
    def get_all_lines_as_dict(self):
        ret = [
            line.to_dict() for line in self.get_all_invoice_lines
        ]

        return ret


class InvoiceLine(models.Model):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    iva_rate = models.DecimalField(max_digits=20, decimal_places=2)
    price_ht = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField()

    @property
    def get_iva_percentage(self):
        return self.iva_rate * 100

    @property
    def get_total_iva(self):
        return self.iva_rate * self.price_ht * self.quantity

    @property
    def get_total_price_ht(self):
        return self.price_ht * self.quantity

    @property
    def get_total_price(self):
        return self.get_total_iva + self.get_total_price_ht

    def to_dict(self):
        return {
            "title": self.title,
            "quantity": str(self.quantity),
            "unit_price": str(self.price_ht),
            "total_price_ht": str(self.get_total_price_ht),
            "total_iva": str(self.get_total_iva),
            "total_price": str(self.get_total_price),
        }

    