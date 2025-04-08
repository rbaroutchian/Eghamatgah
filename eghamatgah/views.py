from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Eghamatgah, EghamatComment
# Create your views here.

class EghamatList(ListView):
    model = Eghamatgah
    paginate_by = 5
    template_name = 'eghamatgah/list.html'
    context_object_name = 'eghamat_list'

    def get_context_data(self, *args, **kwargs):
        context = super(EghamatList, self).get_context_data(*args, **kwargs)
        return context

class EghamatDetail(DetailView):
    model = Eghamatgah
    template_name = 'eghamatgah/detail.html'
    context_object_name = 'eghamat'

    def get_queryset(self):
        query = super(EghamatDetail, self).get_queryset()
        return query

    def get_context_data(self, **kwargs):
        context = super(EghamatDetail, self).get_context_data(**kwargs)
        eghamat : Eghamatgah = kwargs.get('object')
        context['comments'] = EghamatComment.objects.filter(eghamat=eghamat, parent=None).order_by('create_date').prefetch_related('parentcomment')
        context['comments_count'] = EghamatComment.objects.filter(eghamat=eghamat).count()

        return context

