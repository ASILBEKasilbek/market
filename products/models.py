from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    # Rang variantlari
    COLOR_CHOICES = [
        ("oq", "Oq"),
        ("qora", "Qora"),
        ("ko'k", "Ko‘k"),
        ("qizil", "Qizil"),
        ("yashil", "Yashil"),
        ("boshqa", "Boshqa"),
    ]

    # Razmer variantlari
    SIZE_CHOICES = [
        ("s", "S"),
        ("m", "M"),
        ("l", "L"),
        ("xl", "XL"),
        ("xxl", "XXL"),
        ("boshqa", "Boshqa"),
    ]

    # Material variantlari
    MATERIAL_CHOICES = [
        ("paxta", "Paxta"),
        ("jun", "Jun"),
        ("ipak", "Ipak"),
        ("sintetik", "Sintetik"),
        ("boshqa", "Boshqa"),
    ]

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Rang
    color_choice = models.CharField(max_length=20, choices=COLOR_CHOICES, default="oq")
    custom_color = models.CharField(max_length=50, blank=True, null=True)

    # Razmer
    size_choice = models.CharField(max_length=20, choices=SIZE_CHOICES, default="m")
    custom_size = models.CharField(max_length=50, blank=True, null=True)

    # Material
    material_choice = models.CharField(max_length=20, choices=MATERIAL_CHOICES, default="paxta")
    custom_material = models.CharField(max_length=50, blank=True, null=True)

    is_on_sale = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Slug avtomatik
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # Helper funksiyalar
    def get_color(self):
        if self.color_choice == "boshqa" and self.custom_color:
            return self.custom_color
        return dict(self.COLOR_CHOICES).get(self.color_choice, self.color_choice)

    def get_size(self):
        if self.size_choice == "boshqa" and self.custom_size:
            return self.custom_size
        return dict(self.SIZE_CHOICES).get(self.size_choice, self.size_choice)

    def get_material(self):
        if self.material_choice == "boshqa" and self.custom_material:
            return self.custom_material
        return dict(self.MATERIAL_CHOICES).get(self.material_choice, self.material_choice)

    def __str__(self):
        return f"{self.name} ({self.get_color()} | {self.get_size()} | {self.get_material()})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user_identifier = models.CharField(max_length=100, blank=True)  # Cookie uchun
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}"


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user_identifier = models.CharField(max_length=100)  # Cookie ID
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user_identifier')

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user_identifier = models.CharField(max_length=100, blank=True)  # cookie yoki login
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user_identifier} on {self.product.name}"
