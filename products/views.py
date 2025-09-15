from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import JsonResponse
from .models import Product, Review, Like
from .forms import ReviewForm
from orders.forms import OrderForm
import asyncio
from telegram_bot import send_order_notification
from .forms import ReviewForm, CommentForm
from .models import Product, Review, Like, Comment


def product_list(request):
    query = request.GET.get('q')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    color = request.GET.get('color')
    size = request.GET.get('size')
    material = request.GET.get('material')
    category = request.GET.get('category')

    products = Product.objects.select_related('category').prefetch_related('images').all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(custom_color__icontains=query) |
            Q(custom_size__icontains=query) |
            Q(custom_material__icontains=query)
        )

    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    if color:
        products = products.filter(Q(color_choice=color) | Q(custom_color__icontains=color))
    if size:
        products = products.filter(Q(size_choice=size) | Q(custom_size__icontains=size))
    if material:
        products = products.filter(Q(material_choice=material) | Q(custom_material__icontains=material))
    if category:
        products = products.filter(category__slug=category)

    return render(request, "products/index.html", {"products": products})



@login_required
def product_detail(request, pk):
    # Mahsulotni chaqirish va kerakli relationlarni oldindan yuklash
    product = get_object_or_404(
        Product.objects.prefetch_related("images", "reviews", "comments"), pk=pk
    )

    # Sharhlar (reviews)
    reviews = product.reviews.all().order_by("-created_at")
    paginator = Paginator(reviews, 5)  # Har 5 tadan sahifalash
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Kommentariyalar
    comments = product.comments.all().order_by("-created_at")

    # Formlar (boshlang‘ich)
    review_form = ReviewForm()
    comment_form = CommentForm()
    order_form = OrderForm()

    # POST requestlarni qayta ishlash
    if request.method == "POST":
        if "review" in request.POST:  # ✅ Sharh
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user_identifier = request.user.username
                review.save()

                # Reytingni yangilash
                avg_rating = product.reviews.aggregate(Avg("rating"))["rating__avg"]
                product.rating = round(avg_rating, 1) if avg_rating else 0.0
                product.save()

                return redirect("product_detail", pk=pk)

        elif "comment" in request.POST:  # ✅ Kommentariya
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.user_identifier = request.user.username
                comment.save()
                return redirect("product_detail", pk=pk)

        elif "order" in request.POST:  # ✅ Buyurtma
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.product = product
                order.user = request.user
                order.save()

                # Telegram bildirishnoma yuborish
                try:
                    asyncio.run(send_order_notification(order))
                except Exception as e:
                    print(f"Telegram xato: {e}")

                return redirect("product_detail", pk=pk)

    # Template ga yuborish
    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "page_obj": page_obj,
            "comments": comments,
            "review_form": review_form,
            "comment_form": comment_form,
            "order_form": order_form,
        },
    )

@login_required
def toggle_like(request, pk):
    product = get_object_or_404(Product, pk=pk)
    user_identifier = request.user.username  # cookie o‘rniga user login ishlatyapti

    like, created = Like.objects.get_or_create(
        product=product,
        user_identifier=user_identifier,
    )
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"liked": liked, "likes_count": product.likes.count()})

    return redirect("product_detail", pk=pk)
