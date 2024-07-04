import csv
import json
from django.shortcuts import render
from django.core.paginator import Paginator
from ..forms import CustomerModelForm, ProductListModelForm
from django.http import HttpResponse
from blog.models import Product
from django.db.models import Q
from ..models import Customer
from django.shortcuts import render, redirect, get_object_or_404
from openpyxl import Workbook
from django.views import View
from django.views.generic import TemplateView

from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


# Create your views here.


# With Function ----------->>>>>


def index(request):
    products = Product.objects.all()
    paginator = Paginator(products, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/index.html', context)


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    attributes = product.get_attributes()

    context = {
        'product': product,
        'attributes': attributes
    }
    return render(request, template_name='blog/product-detail.html', context=context)


# for the  Customer --->>>.

def customers(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    search_query = request.GET.get('search')
    if search_query:
        page_obj = Customer.objects.filter(Q(name__icontains=search_query) | (Q(email__icontains=search_query)))
    else:
        customers = Customer.objects.all()
    context = {

        'page_obj': page_obj,
    }
    return render(request, 'blog/customers.html', context)


def customers_detail(request, pk):
    customer = Customer.objects.get(id=pk)
    context = {
        'customer': customer
    }
    return render(request, 'blog/customer-details.html', context)


def add_customer(request):
    customers = Customer.objects.all()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CustomerModelForm(request.GET)

    context = {
        'customers': customers,
        'form': form
    }
    return render(request, 'blog/customer/add-customer.html', context)


def delete_customer(request, pk):
    customer = Customer.objects.filter(id=pk).first()
    if customer:
        customer.delete()
        return redirect('customers')


def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers_detail', pk)

    context = {
        'form': form,
        'customer': customer
    }
    return render(request, 'blog/update-customer.html', context)


def export_data(request):
    format = request.GET.get('format', 'csv')
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment ; filename = "customers.csv" '
        writer = csv.writer(response)
        writer.writerow(['id', 'name', 'email', 'phone', 'billing_address'])
        for customer in Customer.objects.all():
            writer.writerow([customer.id, customer.name, customer.email, customer.phone, customer.billing_address])
    elif format == 'json':
        response = HttpResponse(content_type='application/json')
        data = list(Customer.objects.values('id', 'name', 'email', 'phone', 'billing_address'))
        response.content = json.dumps(data, indent=4)
        response['Content-Disposition'] = 'attachment ; filename = "customers.json" '
    elif format == 'xlsx':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customers.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Customers"
        headers = ["Id", "Name", "Email", "Phone", 'Billing_address']
        ws.append(headers)
        customers = Customer.objects.all()
        for customer in customers:
            ws.append([customer.id, customer.name, customer.email, customer.phone, customer.billing_address])
        wb.save(response)
    else:
        response = HttpResponse(status=404)
        response.content('Bad requests')
    return response
