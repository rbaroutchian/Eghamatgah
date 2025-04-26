from django.http import JsonResponse
from .forms import ContactModelForm
from django.views.generic.edit import CreateView


class contactView(CreateView):
    form_class = ContactModelForm
    template_name = 'contact/contact_page.html'
    success_url = '/contact/'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "status": "success",
                "message": "پیام شما با موفقیت ارسال شد!"
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "status": "error",
                "message": "لطفاً تمام فیلدها را به درستی پر کنید."
            }, status=400)
        return super().form_invalid(form)


