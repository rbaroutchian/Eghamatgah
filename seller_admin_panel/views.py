from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from eghamatgah.models import Eghamatgah, Eghamatgah_Category
from eghamatgah.forms import EghamatForm
from django.urls import reverse_lazy
from utils.my_decoretors import permission_checker_decorator_factory


@permission_checker_decorator_factory({'permission': 'admin_index'})
def home(request):
    return render(request, 'home/index.html')


def seller_dashboard(request):
    return render(request, 'eghamatgah/seller_dashboard.html')


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



