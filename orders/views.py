from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order

@staff_member_required
def order_list(request):
    # 'user' ni o'chiramiz, faqat product bilan bog'lamiz
    orders = Order.objects.select_related('product').order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})
