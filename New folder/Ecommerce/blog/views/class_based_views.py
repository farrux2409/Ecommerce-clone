import csv
import json

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from blog.forms import CustomerModelForm, ProductListModelForm, LoginForm, RegisterForm
from django.http import HttpResponse
from blog.models import Product
from django.db.models import Q
from ..models import Customer
from django.shortcuts import render, redirect, get_object_or_404
from openpyxl import Workbook
from django.views import View
from django.views.generic import TemplateView

from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin


# With Class Based  View ---->>

# class ProductList(View):
#     def get(self,request):
#         products = Product.objects.all()
#         paginator =  Paginator(products,2)
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         return render(request,'blog/product/index.html',{'page_obj':page_obj})


# class ProductDetailView(View):
#     def get(self,request,slug):
#         product = Product.objects.get(slug=slug)
#         attributes  = product.get_attributes()
#         context = {
#             'product':product,
#             'attributes':attributes
#         }
#         return render(request,'blog/product/product-detail.html',context)

# class ProductAddView(View):
#     def get(self,request):
#         form = ProductListModelForm()
#         return render(request,'blog/product/add-product.html',{'form':form})
#     def post(self,request):
#         form = ProductListModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')

#         return render(request,'blog/product/add-product.html',{'form':form})


class ProductUpdateView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        form = ProductListModelForm(instance=product)
        return render(request, 'blog/product/update-product.html', {'form': form})

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        form = ProductListModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')

        return render(request, 'blog/product/update-product.html', {'form': form})


class CustomersView(View):
    def get(self, request):
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
        return render(request, 'blog/customer/customers.html', context)


class CustomerDetailView(View):
    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        context = {
            'customer': customer
        }
        return render(request, 'blog/customer/customer-details.html', context)


class CustomerAddView(View):
    def get(self, request):
        form = CustomerModelForm()
        return render(request, 'blog/customer/add-customer.html', {'form': form})

    def post(self, request):
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')
        return render(request, 'blog/customer/add-customer.html', {'form': form})


class CustomerUpdateView(View):
    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        form = CustomerModelForm(instance=customer)
        return render(request, 'blog/customer/update-customer.html', {'form': form})

    def post(self, request, pk):
        customer = Customer.objects.get(id=pk)
        form = CustomerModelForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')

        return render(request, 'blog/customer/update-customer.html', {'form': form})


# With class Based TemplateView ----->>>

class ProductListTemplateView(TemplateView):
    template_name = 'blog/product/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        paginator = Paginator(products, 2)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class ProductDetailTemplateView(TemplateView):
    template_name = 'blog/product/product-detail.html'

    def get_contex_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=kwargs['slug'])
        attributes = Product.get_attributes()
        context['product'] = product
        context['attributes'] = attributes
        return context


class ProductAddTemplateView(TemplateView):
    template_name = 'blog/product/add-product.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductListModelForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ProductListModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


# Shu class da xatolik buldi shunga
class ProductUpdateTemplateView(TemplateView):
    template_name = 'blog/product/update-product.html'

    def get_contex_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=kwargs['slug'])
        context['product'] = product
        context['form'] = ProductListModelForm(instance=product)
        return context

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        form = ProductListModelForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('index')


class CustomerListTemplateView(TemplateView):
    template_name = 'blog/customer/customers.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = Customer.objects.all()
        paginator = Paginator(customers, 5)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        search_query = self.request.GET.get('search')
        if search_query:
            page_obj = Customer.objects.filter(Q(name__icontains=search_query) | (Q(email__icontains=search_query)))
        else:
            customers = Customer.objects.all()
        context['page_obj'] = page_obj
        return context
    # def get():
    #     pass


class CustomerDetailTemplateView(TemplateView):
    template_name = 'blog/customer/customer-details.html'

    def get_contex_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(id=kwargs['pk'])
        context['customer'] = customer
        return context


class CustomerAddTemplateView(TemplateView):
    template_name = 'blog/customer/add-customer.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomerModelForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')


class CustomerUpdateTemplateView(TemplateView):
    template_name = 'blog/customer/update-customer.html'

    def get_contex_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Customer.objects.get(id=kwargs['pk'])
        context['form'] = ProductListModelForm(instance=product)
        return context

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=kwargs['pk'])
        form = ProductListModelForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            return redirect(('customers'))


# With create,list,update,delete --------->>>> homework


class ProductListView(ListView):
    model = Product
    template_name = 'blog/product/index.html'
    context_object_name = 'page_obj'
    paginate_by = 2


class ProductCreateView(CreateView):
    form_class = ProductListModelForm
    model = Product
    template_name = 'blog/product/add-product.html'
    success_url = reverse_lazy('index')
    context_object_name = 'page'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'blog/product/product-detail.html'


class ProductUpdateView1(UpdateView):
    model = Product
    template_name = 'blog/product/update-product.html'
    form_class = ProductListModelForm
    success_url = reverse_lazy('index')


class ProductDeleteView(DeleteView):
    model = Product


class CustomerListView(ListView):
    model = Customer
    template_name = 'blog/customer/customers.html'
    context_object_name = 'page_obj'
    paginate_by = 2

    def get_queryset(self):
        self.queryset = super(CustomerListView, self).get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            self.queryset = Customer.objects.filter(
                Q(name__icontains=search_query) | (Q(email__icontains=search_query)))
        else:
            self.queryset = Customer.objects.all()
        return self.queryset


class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'blog/customer/add-customer.html'
    form_class = CustomerModelForm
    success_url = reverse_lazy('customers')


class CustomerDetailView1(DetailView):
    model = Customer
    template_name = 'blog/customer/customer-details.html'


class CustomerUpdateView1(UpdateView):
    model = Customer
    template_name = 'blog/customer/update-customer.html'
    form_class = CustomerModelForm
    success_url = reverse_lazy('customers')


class CustomerDeleteView1(DeleteView):
    model = Customer
    template_name = "blog/customer/delete.html"
    success_url = reverse_lazy('customers')


class CustomerDeleteView2(DeleteView):
    model = Customer

    success_url = reverse_lazy('customers')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class DeleteCustomerTemplateView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ExportDataView(View):
    def get(self, request):
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


# for the Auth Homework --->>>
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages


class CustomLoginView(View):
    template_name = 'blog/auth/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, {'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('index')
        message = 'Invalid Credentials'
        return render(request, self.template_name, {'form': form, 'message': message})


class CustomLogoutView(View):
    def get(self, request):
        if request.method == 'GET':
            logout(request)
            return redirect(reverse('index'))
        return render(request, 'blog/auth/logout.html')


from django.contrib.auth.forms import UserCreationForm

# class CustomerRegisterView(UserCreationForm):
#     class Meta:
#         model = Customer
#         form_class = CustomerModelForm
from django.contrib.messages.views import SuccessMessageMixin

# class CustomerRegisterView(CreateView):
#     template_name = "blog/auth/register.html"
#     success_url = reverse_lazy("index")
#     form_class = RegisterForm
#     success_message = "You have successfully registered."


from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from blog.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from blog.views.tokens import account_activation_token
from django.core.mail import EmailMessage


class CustomerRegisterView(View):
    template_name = "blog/auth/register.html"
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(first_name=first_name, email=email, password=password)
            user.is_active = False
            user.is_staff = True
            user.is_superuser = True
            user.save()
            current_site = get_current_site(request)
            subject = 'Verify your account '
            message = render_to_string('blog/auth/email/activation.html',
                                       {
                                           'request': request,
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.id)),
                                           'token': account_activation_token.make_token(user)
                                       })

            email = EmailMessage(subject, message, to=[email])
            email.content_subtype = 'html'
            email.send()
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('verify_email_done')

            # login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            # return redirect('login')

        return render(request, 'blog/auth/register.html', {'form': form})
