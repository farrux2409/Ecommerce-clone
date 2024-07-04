from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse

from blog.forms import LoginForm, RegisterForm, EmailForm
from blog.models import User
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL

# email verify 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
# from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from blog.views.tokens import account_activation_token


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
            else:
                messages.add_message(
                    request,
                    level=messages.WARNING,
                    message='User not found'

                )

    return render(request, 'blog/auth/login.html', {'form': form})


def logout_page(request):
    if request.method == 'GET':
        logout(request)
        return redirect(reverse('index'))
    return render(request, 'blog/auth/logout.html')


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
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


def sending_email(request):
    sent = False

    if request.method == 'POST':
        form = EmailForm(request.POST)
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = request.POST.get('from_email')
        to = request.POST.get('to')
        send_mail(subject, message, from_email, [to])
        sent = True

    return render(request, 'blog/sending-email.html', {'form': form, 'sent': sent})


def verify_email_done(request):
    return render(request, 'blog/auth/email/verify-email-done.html')


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('verify_email_complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'blog/auth/email/verify-email-confirm.html')


def verify_email_complete(request):
    return render(request, 'blog/auth/email/verify-email-complete.html')
