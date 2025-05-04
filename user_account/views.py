from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView

from user_account.forms import LoginForm, RegisterForm
from user_account.models import User
from utils.sms import send_verification_sms
from .task import send_verification_sms_async
from .forms import EditProfileModelForm
from django.contrib import messages
from booking.models import Booking




# Create your views here
class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'user/login_page.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data.get('username')
            user_pass = login_form.cleaned_data.get('Password')
            user: User = User.objects.filter(username__iexact=user_name).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('username', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse_lazy('home'))
                    else:
                        login_form.add_error('username', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error('username', 'کاربری با مشخصات وارد شده یافت نشد')
        context = {
            'login_form': login_form
        }

        return render(request, 'user/login_page.html', context)


class Register(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'user/register_page.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')
            user_number = register_form.cleaned_data.get('user_number')
            password = register_form.cleaned_data.get('password')

            user_exist = User.objects.filter(username=user_name).exists()
            if user_exist:
                register_form.add_error('username', 'نام کاربری قبلاً ثبت شده است.')
            else:
                verification_code = get_random_string(length=6, allowed_chars='0123456789')

                new_user = User(
                    username=user_name,
                    email=email,
                    user_number=user_number,
                    is_active=False,
                    verification_code=verification_code
                    )
                new_user.set_password(password)
                new_user.save()
                # send_verification_sms_async.delay(user_number, verification_code)

                # return redirect(reverse('verify_code_page'))

        context = {
            'register_form': register_form
        }
        return render(request, 'user/profile.html', context)


class VerifyCodeView(View):
    def get(self, request):
        return render(request, 'user/verify_code.html')

    def post(self, request):
        user_number = request.session.get('user_number')
        code = request.POST.get('verification_code')

        try:
            user = User.objects.get(user_number=user_number, verification_code=code)
            user.is_active = True
            user.verification_code = ''
            user.save()
            login(request, user)

            return redirect('home')
        except User.DoesNotExist:
            error = 'کد وارد شده اشتباه است.'
            return render(request, 'user/verify_code.html', {'error': error})




def user_logout(request):
    logout(request)
    return redirect('home')


@method_decorator(login_required, name='dispatch')
class EditUserProfilePage(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        user_bookings = Booking.objects.filter(user=request.user).select_related('eghamat')
        context = {
            'form': edit_form,
            'current_user': current_user,
            'bookings': user_bookings,
        }
        return render(request, 'user/profile.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            # edit_form.save(commit=True)
            edit_form.save()
            messages.success(request, "اطلاعات با موفقیت ذخیره شد.")
            return redirect('profile')
        user_bookings = Booking.objects.filter(user=request.user).select_related('eghamat')


        context = {
            'form': edit_form,
            'current_user': current_user,
            'bookings': user_bookings,
        }
        return render(request, 'user/profile.html', context)


