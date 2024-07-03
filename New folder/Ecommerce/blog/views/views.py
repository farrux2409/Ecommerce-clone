import csv
import json
from django.shortcuts import render
from django.core.paginator import Paginator
from ..forms import CustomerModelForm,ProductListModelForm
from django.http import HttpResponse
from blog.models import Product
from django.db.models import Q
from ..models import Customer
from django.shortcuts import render, redirect
from openpyxl import Workbook
from django.views import View
from django.views.generic import TemplateView

from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
# Create your views here.


# With Function ----------->>>>>


# def index(request):
#     products = Product.objects.all()
#     paginator = Paginator(products, 2)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj,
#     }
#     return render(request, 'blog/index.html', context)



# def product_detail(request, slug):
#     product = Product.objects.get(slug=slug)
#     attributes = product.get_attributes()

#     context = {
#         'product': product,
#         'attributes': attributes
#     }
#     return render(request, template_name='blog/product-detail.html', context=context)

# for the  Customer --->>>.

# def customers(request):
#     customers = Customer.objects.all()
#     paginator = Paginator(customers, 5)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     search_query = request.GET.get('search')
#     if search_query:
#         page_obj= Customer.objects.filter(Q(name__icontains=search_query)|(Q(email__icontains = search_query)))
#     else:
#         customers = Customer.objects.all()
#     context = {
        
#         'page_obj': page_obj,
#     }
#     return render(request, 'blog/customers.html', context)


# def customers_detail(request, pk):
#     customer = Customer.objects.get(id=pk)
#     context = {
#         'customer': customer
#     }
#     return render(request, 'blog/customer-details.html', context)


# def add_customer(request):
#     customers = Customer.objects.all()
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#     else:
#         form = CustomerModelForm(request.GET)

#     context = {
#         'customers': customers,
#         'form': form
#     }
#     return render(request, 'blog/customer/add-customer.html', context)

def delete_customer(request, pk):
    customer = Customer.objects.filter(id=pk).first()
    if customer:
        customer.delete()
        return redirect('customers')



# def update_customer(request,pk):
#     customer = Customer.objects.get(id = pk)
#     form = CustomerModelForm(instance=customer)
#     if request.method =='POST':
#            form = CustomerModelForm(request.POST, request.FILES, instance=customer)
#            if form.is_valid():
#                form.save()
#                return redirect('customers_detail', pk)
           
#     context = {
#         'form': form,
#         'customer': customer
#     }
#     return render(request, 'blog/update-customer.html', context)



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
    def get(self,request,slug):
        product = Product.objects.get(slug=slug)
        form = ProductListModelForm(instance=product)
        return render(request,'blog/product/update-product.html',{'form':form})
    

    def post(self,request,slug):
        product = Product.objects.get(slug=slug)
        form = ProductListModelForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')
        

        return render(request,'blog/product/update-product.html',{'form':form})
       








class CustomersView(View):
    def get(self,request):
        customers = Customer.objects.all()
        paginator = Paginator(customers, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        search_query = request.GET.get('search')
        if search_query:
            page_obj= Customer.objects.filter(Q(name__icontains=search_query)|(Q(email__icontains = search_query)))
        else:
            customers = Customer.objects.all()
        context = {
            
            'page_obj': page_obj,
        }
        return render(request, 'blog/customer/customers.html', context)






class CustomerDetailView(View):
    def get(self,request,pk):
        customer = Customer.objects.get(id=pk)
        context = {
            'customer': customer
        }
        return render(request, 'blog/customer/customer-details.html', context)





class CustomerAddView(View):
    def get(self,request):
        form = CustomerModelForm()
        return render(request,'blog/customer/add-customer.html',{'form':form})
    
    def post(self,request):
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')
        return render(request,'blog/customer/add-customer.html',{'form':form})








               
        
        

class CustomerUpdateView(View):
    def get(self,request,pk):
        customer = Customer.objects.get(id = pk)
        form  = CustomerModelForm(instance=customer)
        return render(request,'blog/customer/update-customer.html',{'form':form})

    def post(self,request,pk):
        customer = Customer.objects.get(id = pk)
        form  = CustomerModelForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')
        
        return render(request,'blog/customer/update-customer.html',{'form':form})



# With class Based TemplateView ----->>>

class ProductListTemplateView(TemplateView):
    template_name = 'blog/product/index.html'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        paginator =  Paginator(products,2)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
        
      


class ProductDetailTemplateView(TemplateView):
    template_name = 'blog/product/product-detail.html'
    
    def get_contex_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug = kwargs['slug'] )
        attributes = Product.get_attributes()  
        context['product'] = product
        context['attributes'] = attributes
        return context


class ProductAddTemplateView(TemplateView):
    template_name = 'blog/product/add-product.html'
    
    def get_context_data(self,*args,**kwargs):
        context  = super().get_context_data(**kwargs)
        context['form'] = ProductListModelForm()
        return context 
    
    def post(self,request,*args,**kwargs):
        form = ProductListModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


# Shu class da xatolik buldi shunga 
class ProductUpdateTemplateView(TemplateView):
    template_name = 'blog/product/update-product.html'
    

    def get_contex_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        product =  Product.objects.get(slug=kwargs['slug'])
        context['form'] = ProductListModelForm(instance=product)
        return context
    
    def post(self,request,*args,**kwargs):
   
        product = Product.objects.get(slug=kwargs['slug'])
        form = ProductListModelForm(request.POST,instance=product)
        
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            context = self.get_context_data()
            context['data_form'] = form
            return render(request, self.template_name, context)

        return self.get(request)
        
    
    
# bu yerda ham xatolik bor 
class CustomersListTemplateView(TemplateView):
    template_name = 'blog/customer/customers.html'
    

    def get_contex_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        customers = Customer.objects.all()
        paginator = Paginator(customers, 5)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        search_query = self.request.GET.get('search')
        
        
        if search_query:
            page_obj= Customer.objects.filter(Q(name__icontains=search_query)|(Q(email__icontains = search_query)))
        else:
            customers = Customer.objects.all()
        
        context['page_obj'] = page_obj
        return context
        

    # def get():
    #     pass

# bunda ham xato bor 

class CustomerDetailTemplateView(TemplateView):
    template_name = 'blog/customer/customer-details.html'

    def get_contex_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(id=kwargs['pk'])
        context['customer'] = customer
        return context
       


class CustomerAddTemplateView(TemplateView):
    template_name = 'blog/customer/add-customer.html'

    def get_context_data(self,*args,**kwargs):
        context  = super().get_context_data(**kwargs)
        context['form'] = CustomerModelForm()
        return context 
    
    def post(self,request,*args,**kwargs):
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')

# bunda ham usha xato product update dagi kabi

class CustomerUpdateTemplateView(TemplateView):
    template_name = 'blog/customer/update-customer.html'


    def get_contex_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        product =  Customer.objects.get(id=kwargs['pk'])
        context['form'] = ProductListModelForm(instance=product)
        return context
    
    def post(self,request,*args,**kwargs):
   
        customer = Customer.objects.get(id=kwargs['pk'])
        form = ProductListModelForm(request.POST,instance=customer)
        
        if form.is_valid():
            form.save()
            return redirect(('customers'))
    


# With create,list,update,delete --------->>>> homework

# shunda pagination borligi uchun ozroq tushunmadim
class ProductListView(ListView):
  
    model = Product
    template_name = 'blog/product/index.html'
    context_object_name = 'page'
    
    
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
    model = Product
    template_name = 'blog/customer/customers.html'
    context_object_name = 'page'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('search')
        
        if q:
            sat_q = Customer.objects.filter(Q(title__icontains=q) | Q(price__icontains=q))
            queryset = queryset.filter(sat_q)
        return queryset


    
    

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


class DeleteCustomerTemplateView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)    



def export_data(request):
    format = request.GET.get('format','csv')
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment ; filename = "customers.csv" '
        writer = csv.writer(response)
        writer.writerow(['id','name','email','phone','billing_address'])
        for customer in Customer.objects.all():
            writer.writerow([customer.id,customer.name,customer.email,customer.phone,customer.billing_address])
    elif format == 'json':
        response = HttpResponse(content_type='application/json')
        data = list(Customer.objects.values('id','name','email','phone','billing_address'))
        response.content = json.dumps(data,indent=4 )
        response['Content-Disposition'] = 'attachment ; filename = "customers.json" '
    elif format == 'xlsx':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customers.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Customers"
        headers = ["Id", "Name", "Email","Phone",'Billing_address']
        ws.append(headers)
        customers = Customer.objects.all()
        for customer in customers:
            ws.append([customer.id,customer.name,customer.email,customer.phone,customer.billing_address])
        wb.save(response)
    else:
        response = HttpResponse(status = 404)
        response.content('Bad requests')
    return response



    


    

