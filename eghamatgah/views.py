from datetime import datetime, timedelta
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django_extensions.db.fields import json

from booking.models import Booking
from .models import Eghamatgah, EghamatComment, UnavailableDate, AvailableDate
from .forms import EghamatCommentForm
from django.http import JsonResponse
from booking.forms import BookingForm
from datetime import timedelta


# Create your views here.

class EghamatList(ListView):
    model = Eghamatgah
    paginate_by = 5
    template_name = 'eghamatgah/list2.html'
    context_object_name = 'eghamat_list'

    def get_context_data(self, *args, **kwargs):
        context = super(EghamatList, self).get_context_data(*args, **kwargs)
        return context

class EghamatDetail(DetailView):
    model = Eghamatgah
    template_name = 'eghamatgah/detail3.html'
    context_object_name = 'eghamat'

    def get_queryset(self):
        query = super(EghamatDetail, self).get_queryset()
        return query

    def get_context_data(self, **kwargs):
        context = super(EghamatDetail, self).get_context_data(**kwargs)
        eghamat = self.object

        available_ranges = AvailableDate.objects.filter(eghamat=eghamat)
        available_days = []
        for r in available_ranges:
            diff = (r.end_date - r.start_date).days
            available_days += [r.start_date + timedelta(days=i) for i in range(diff+1)]

        bookings = Booking.objects.filter(eghamat=eghamat, status='confirmed')
        reserved_days = []
        for b in bookings:
            diff= (b.check_out - b.check_in).days
            reserved_days += [b.check_in + timedelta(days=i) for i in range(diff+1)]

        final_available = [d.isoformat() for d in available_days if d not in reserved_days]
        final_reserved = [d.isoformat() for d in reserved_days]

        context.update({
            'comments': EghamatComment.objects.filter(eghamat=eghamat, parent=None)
            .order_by('create_date')
            .prefetch_related('parentcomment'),
            'comments_count': EghamatComment.objects.filter(eghamat=eghamat).count(),
            'comment_form': EghamatCommentForm,
            'booking_form': BookingForm(),
            'available_dates': final_available,
            'reserved_dates': final_reserved,
            'total_price': None,
        })

        # context['comments'] = EghamatComment.objects.filter(eghamat=eghamat, parent=None).order_by('create_date').prefetch_related('parentcomment')
        # context['comments_count'] = EghamatComment.objects.filter(eghamat=eghamat).count()
        # context['comment_form']= EghamatCommentForm
        # context['booking_form'] = BookingForm
        # context['total_price']= None

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        eghamat = self.object



        form = EghamatCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.eghamat = self.object
            comment.user = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent = get_object_or_404(EghamatComment, id=parent_id)
                comment.parent = parent
            comment.save()
            return redirect('eghamat_detail', pk=self.object.pk)

        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.eghamat = eghamat

            check_in = booking.check_in
            check_out = booking.check_out
            days = (check_out - check_in).days
            requested_dates = [check_in + timedelta(days=i) for i in range(days + 1)]

            available_ranges = AvailableDate.objects.filter(eghamat=eghamat)
            available_days = []
            for r in available_ranges:
                diff = (r.end_date - r.start_date).days
                available_days += [
                    r.start_date + timedelta(days=i)
                    for i in range(diff + 1)
                ]

            if not all(d in available_days for d in requested_dates):
                messages.error(request, 'بازه انتخاب‌شده در بین تاریخ‌های قابل رزرو نیست.')
                return redirect('eghamat_detail', pk=eghamat.pk)

            overlap = UnavailableDate.objects.filter(eghamat=eghamat, date__in=requested_dates).exists()
            if overlap:
                messages.error(request, 'برخی از تاریخ‌های انتخابی قبلاً رزرو شده‌اند.')
                return redirect('eghamat_detail', pk=eghamat.pk)

            capacity = self.object.zarfiat or 0
            extra_price_per_person = self.object.zarfiat_extra or 0
            base_price_per_night = self.object.gheymat_har_shab or 0
            total_guests = booking.persons or 0
            extra_guests = max(0, total_guests - capacity)

            nights = (booking.check_out - booking.check_in).days
            extra_total = extra_guests * extra_price_per_person
            total_price = (base_price_per_night + extra_total) * nights

            booking.total_price = total_price
            booking.save()

            # ذخیره UnavailableDate
            for d in requested_dates:
                UnavailableDate.objects.create(eghamat=eghamat, date=d)


            messages.success(request, 'رزرو با موفقیت انجام شد.')
            return redirect('eghamat_detail', pk=eghamat.pk)

        context = self.get_context_data()
        context['comment_form'] = form
        context['booking_form'] = booking_form
        return render(request, self.template_name, context)





def calculate_price(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        eghamat = get_object_or_404(Eghamatgah, pk=pk)

        persons = int(request.GET.get('persons', 0))
        check_in = request.GET.get('check_in', None)
        check_out = request.GET.get('check_out', None)

        if persons and check_in and check_out:
            capacity = eghamat.zarfiat or 0
            extra_price_per_person = eghamat.zarfiat_extra or 0
            base_price_per_night = eghamat.gheymat_har_shab or 0

            extra_guests = max(0, persons - capacity)
            nights = (datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days
            extra_total = extra_guests * extra_price_per_person
            total_price = (base_price_per_night + extra_total) * nights

            return JsonResponse({'total_price': total_price})
        else:
            return JsonResponse({'error': 'اطلاعات ناقص است'}, status=400)

    return JsonResponse({'error': 'درخواست معتبر نیست'}, status=400)


