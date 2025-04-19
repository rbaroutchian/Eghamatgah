from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.views.generic import ListView
from eghamatgah.models import Eghamatgah
from booking.models import Booking

# Create your views here.
def home(request):
    return render(request, 'base2.html')


class EghamatgahSearchView(ListView):
    model = Eghamatgah
    template_name = 'eghamatgah/search_shahr.html'
    context_object_name = 'eghamatgahs'
    paginate_by = 10

    def get_queryset(self):
        queryset = Eghamatgah.objects.all()

        shahr = self.request.GET.get('shahr')
        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')
        persons = self.request.GET.get('zarfiat')

        if shahr:
            queryset = queryset.filter(shahr__icontains=shahr)

        if persons and persons.isdigit():
            queryset = queryset.filter(zarfiat__gte=int(persons))

        if check_in and check_out:
            parsed_check_in = parse_date(check_in)
            parsed_check_out = parse_date(check_out)

            if parsed_check_in and parsed_check_out:
                reserved_ids = Booking.objects.filter(
                    check_in__lt=parsed_check_out,
                    check_out__gt=parsed_check_in
                ).values_list('eghamat_id', flat=True)

                queryset = queryset.exclude(id__in=reserved_ids)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shahr'] = self.request.GET.get('shahr', '')
        context['check_in'] = self.request.GET.get('check_in', '')
        context['check_out'] = self.request.GET.get('check_out', '')
        context['persons'] = self.request.GET.get('zarfiat', '')
        return context


def site_footer(request):
    return render(request, 'footer_component.html')
