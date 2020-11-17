from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.generic import ListView, DetailView, CreateView
from django.template.response import TemplateResponse
from django.urls import reverse
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect

from .serializers import ClientSerializer, InvoiceSerializer
from .models import Client, Invoice, InvoiceLine
from .forms import ClientForm, InvoiceForm

# Create your views here.

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def retrieve(self, request, *args, **kwargs):
      def get_invoice_urls(client):
          invoices = client.get_all_invoices
          dict_ret = [
              {"id": invoice.invoice_id, "url": reverse("invoice-detail", args=[invoice.invoice_id])}
              for invoice in invoices
          ]
          return dict_ret
      instance = self.get_object()
      serializer = self.get_serializer(instance)
      data = serializer.data
      data = {
          **data,
          "invoices_url": get_invoice_urls(instance)
      }
      return Response(data)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class ClientList(ListView):
    model = Client

class ClientDetail(DetailView):
    model = Client
    def get_context_data(self, **kwargs):
        context = super(ClientDetail, self).get_context_data(**kwargs)
        client = context["object"]
        context['invoices'] = client.get_all_invoices
        return context

class InvoiceDetail(DetailView):
    model = Invoice
    def get_context_data(self, **kwargs):
        context = super(InvoiceDetail, self).get_context_data(**kwargs)
        invoice = context["object"]
        context['invoice_lines'] = invoice.get_all_invoice_lines
        return context

def client_new(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/clients/')
    else:
        form = ClientForm()
    return render(request, 'test_app/client_new.html', {'form': form})


InvoiceLineFormSet = inlineformset_factory(Invoice, InvoiceLine, fields=('title', 'quantity', 'iva_rate', 'price_ht'), extra=10, min_num=1)

class InvoiceNew(CreateView):

    form_class = InvoiceForm
    model = Invoice
    success_url = "/invoices/new/"
    
    def get(self, request, *args, **kwargs):
        
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        invoice_item_form = InvoiceLineFormSet()
        return self.render_to_response(self.get_context_data(form=form, invoice_item_form=invoice_item_form))
    
    def post(self, request, *args, **kwargs):
      
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        invoice_item_form = InvoiceLineFormSet(self.request.POST)
         
        if form.is_valid() and invoice_item_form.is_valid():
            return self.form_valid(form, invoice_item_form)
        else:
            return self.form_invalid(form, invoice_item_form)
        
    def form_valid(self, form, product_item_form):
        
        self.object = form.save()
        product_item_form.instance = self.object
        product_item_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, invoice_item_form):
        
        return self.render_to_response(self.get_context_data(form=form, invoice_item_form=invoice_item_form))