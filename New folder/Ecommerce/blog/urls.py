from django.contrib import admin
from django.urls import path

from blog.views.class_based_views import (
    ProductListTemplateView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateTemplateView,
    CustomersView,
    CustomerDetailView1,
    CustomerDeleteView2,
    CustomerAddView,
    CustomerUpdateView1,
    ExportDataView, CustomerListView,

)

from blog.views.auth import (
    login_page,
    logout_page,
    register,
    sending_email,
    verify_email_done,
    verify_email_complete,
    verify_email_confirm
)
from blog.views.class_based_views import (
    CustomLoginView,
    CustomLogoutView,
    CustomerRegisterView,

)

urlpatterns = [
    # Product urls
    path('', ProductListTemplateView.as_view(), name='index'),
    path('detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-product/', ProductCreateView.as_view(), name='add-product'),
    path('update-product/<slug:slug>/', ProductUpdateTemplateView.as_view(), name='update_product'),

    # Customers urls
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customers_detail/<int:pk>/', CustomerDetailView1.as_view(), name='customers_detail'),
    path('delete/<int:pk>', CustomerDeleteView2.as_view(), name='delete'),
    path('add-customer/', CustomerAddView.as_view(), name='add_customers'),
    path('customer/<int:pk>/', CustomerUpdateView1.as_view(), name='update_customer'),
    # authentication's url
    path('login-page/', CustomLoginView.as_view(), name='login'),
    path('logout-page/', CustomLogoutView.as_view(), name='logout'),
    path('register-page/', CustomerRegisterView.as_view(), name='register'),
    # sending email url
    path('sending-email-url/', sending_email, name='sending_email'),
    #  verify email url
    path('verify-email-done/', verify_email_done, name='verify_email_done'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify_email_confirm'),
    path('verify-email/complete/', verify_email_complete, name='verify_email_complete'),

    # exporting data
    path('customers-export-data-downloads', ExportDataView.as_view(), name='export_data'),

]
