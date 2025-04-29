from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import IntegerField, Avg, Sum
from django.db.models.functions import Cast
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView, View
from eghamatgah.models import Eghamatgah, Eghamatgah_Category, EghamatComment
from eghamatgah.forms import EghamatForm, EghamatCommentFormAdmin
from django.urls import reverse_lazy

from seller_account.forms import SellerProfileForm
from user_account.models import User
from utils.my_decoretors import permission_checker_decorator_factory
from booking.models import Booking
from django.utils import timezone
from datetime import timedelta


@permission_checker_decorator_factory({'permission': 'admin_index'})
def home(request):
    eghamatgah_count = Eghamatgah.objects.count()
    eghamatgah_comment = EghamatComment.objects.count()
    avg_star = EghamatComment.objects.annotate(
        star_int=Cast('star', IntegerField())
    ).aggregate(
        avg_star_value=Avg('star_int')
    )['avg_star_value']
    one_month_ago = timezone.now() - timedelta(days=30)
    recent_booking_count = Booking.objects.filter(
        created_at__gte=one_month_ago
    ).count()
    recent_booking = Booking.objects.filter(created_at__gte=one_month_ago)
    today = timezone.now().date()
    daramad = Booking.objects.filter(created_at__gte=one_month_ago).aggregate(total_daramad=Sum('total_price'))[
                  'total_daramad'] or 0
    context = {
        'eghamatgah_count':eghamatgah_count,
        'eghamatgah_comment':eghamatgah_comment,
        'avg_star':avg_star,
        'recent_booking_count':recent_booking_count,
        'recent_booking':recent_booking,
        'today':today,
        'daramad':daramad
    }
    return render(request, 'home/index.html',context)

def sidebarview(request):
    user = User.objects.all()
    context = {
        'user':user
    }
    return render(request, 'include/sidebar.html', context)


@method_decorator(login_required, name='dispatch')
class EditSellerProfilePage(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = SellerProfileForm(instance=request.user.seller)
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'profile/seller_profile.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = SellerProfileForm(request.POST, request.FILES, instance=request.user.seller)
        if edit_form.is_valid():
            edit_form.save(commit=True)

        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'profile/seller_profile.html', context)


@method_decorator(permission_checker_decorator_factory({'permission': 'eghamat_list'}), name='dispatch')
class EghamatgahList(ListView):
    model = Eghamatgah
    paginate_by = 12
    template_name = 'eghamatgah/eghamat_list_dashboard.html'


    def get_context_data(self, *args, **kwargs):
        context = super(EghamatgahList, self).get_context_data(*args, **kwargs)

        for eghamat in context['object_list']:
            eghamat.comment_count = eghamat.eghamatcomment_set.count()
        return context

    def get_queryset(self):
        query = super(EghamatgahList, self).get_queryset()
        # category_name = self.kwargs.get('category')
        # if category_name is not None:
        #     query = query.filter(selected__categories__url__title__iexact=category_name)
        return query


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class Eghamatgah_add(CreateView):
    model = Eghamatgah
    form_class = EghamatForm
    template_name = 'eghamatgah/add_eghamatgah.html'
    success_url = reverse_lazy('eghamat_list_dashboard')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class Eghamatgah_Category_admin(ListView):
    model = Eghamatgah_Category
    template_name = 'eghamatgah/category.html'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(Eghamatgah_Category_admin, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(Eghamatgah_Category_admin, self).get_queryset()
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected__categories__url__title__iexact=category_name)
        return query


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class Eghamatgah_Detail(UpdateView):
    model = Eghamatgah
    template_name = 'eghamatgah/detail_eghamat_admin.html'
    form_class = EghamatForm
    success_url = reverse_lazy('eghamat_list_dashboard')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class Eghamatgah_Delete(DeleteView):
    model = Eghamatgah
    template_name = 'eghamatgah/eghamat_list_dashboard.html'
    success_url = reverse_lazy('eghamat_list_dashboard')


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class Category_Delete(DeleteView):
    model = Eghamatgah_Category
    template_name = 'eghamatgah/category.html'
    success_url = reverse_lazy('category_eghamat')


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class booking_eghamat(ListView):
    model = Booking
    paginate_by = 12
    template_name = 'booking/booking.html'

    def get_context_data(self, *args, **kwargs):
        context = super(booking_eghamat, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        query = super(booking_eghamat, self).get_queryset()
        return query


@method_decorator(permission_checker_decorator_factory(), name='dispatch')
class EghamatCommentAdmin(ListView):
    model = EghamatComment
    form_class = EghamatCommentFormAdmin
    template_name = 'eghamatgah/comments.html'
    success_url = reverse_lazy('comment_list')

    def get_queryset(self):
        query = super(EghamatCommentAdmin, self).get_queryset()
        status = self.request.GET.get('status')
        eghamat_id = self.request.GET.get('eghamat')

        if status:
            query = query.filter(status=status)
        if eghamat_id:
            query = query.filter(eghamat__id=eghamat_id)

        return query.order_by('-create_date')


@permission_checker_decorator_factory()
def daramad_view(request):
    bookings = Booking.objects.filter(status='confirmed').order_by('-created_at')
    total_income = bookings.aggregate(total=models.Sum('total_price'))['total'] or 0
    context = {
        'bookings': bookings,
        'total_income': total_income,
    }
    return render(request, 'daramad/daramad.html', context)


def daramad_ajax(request):
    period = request.GET.get('period', 'this_month')  # دریافت انتخاب کاربر

    now = timezone.now()

    if period == 'this_month':
        start_date = now.replace(day=1)
    elif period == 'last_month':
        start_date = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
    elif period == '3_months':
        start_date = now - timedelta(days=90)
    elif period == '6_months':
        start_date = now - timedelta(days=180)
    elif period == 'this_year':
        start_date = now.replace(month=1, day=1)
    else:
        start_date = now.replace(day=1)  # پیش‌فرض ماه جاری

    bookings = Booking.objects.filter(status='paid', created__gte=start_date).order_by('-created_at')

    total_income = bookings.aggregate(total=Sum('total_price'))['total'] or 0

    booking_list = []
    for booking in bookings:
        booking_list.append({
            'created': booking.created_at.strftime('%Y/%m/%d'),
            'code': booking.id,
            'guest_name': booking.user.first_name,
            'total_price': f"{booking.total_price:,}",
            'status': 'پرداخت شده' if booking.status == 'confirmed' else 'در انتظار پرداخت',
        })

    return JsonResponse({
        'total_income': f"{total_income:,}",
        'bookings': booking_list
    })
