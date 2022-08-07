from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView, TemplateView

from app_shop.models import Order


class ShowOrders(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        orders = Order.objects.filter(buyer__username='admin').prefetch_related('cart')
        kwargs.update({
            'orders': orders
        })
        return super().get_context_data(**kwargs)
