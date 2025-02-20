from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from userauths.models import Profile, User
from vendor.models import Vendor


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="category",
                             default="category.jpg", null=True, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Category"
        ordering = ['title']

    # def save(self, *args, **kwargs):
    #     if self.slug == "" or self.slug == None:
    #         self.slug = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)


class Product(models.Model):

    STATUS = (
        ("draft", "Draft"),
        ("disable", "Disable"),
        ("in_review", "In Review"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="products",
                             default="product.jpg", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    old_price = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00)
    shipping_amount = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00)
    stock_qty = models.PositiveBigIntegerField(default=1)
    in_stock = models.BooleanField(default=True)
    status = models.CharField(
        max_length=100, choices=STATUS, default="published")
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    pid = ShortUUIDField(unique=True, length=10, alphabet="abcdefg12345")
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if self.slug == "" or self.slug == None:
    #         self.slug = slugify(self.title)
    #     super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def product_rating(self):
        product_rating = Review.objects.filter(
            product=self).aggregate(avg_rating=models.Avg("rating"))
        return product_rating["avg_rating"]

    def rating_count(self):
        return Review.objects.filter(product=self).count()

    def gallery(self):
        return Gallery.objects.filter(product=self)

    def color(self):
        return Color.objects.filter(product=self)

    def specification(self):
        return Specification.objects.filter(product=self)

    def size(self):
        return Size.objects.filter(product=self)

    # def save(self, *args, **kwargs):
    #     self.rating = self.product_rating()
    #     super(Product, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        rating_value = self.product_rating()
        self.rating = rating_value if rating_value is not None else 0

        super(Product, self).save(*args, **kwargs)


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to="gallery", default="gallery.jpg")
    active = models.BooleanField(default=True)
    gid = ShortUUIDField(unique=True, length=10, alphabet="abcdefg12345")

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name_plural = "Products Images"


class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class Size(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)

    def __str__(self):
        return self.name


class Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    color_code = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    sub_total = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    service_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    country = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    cart_id = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart_id} - {self.product.title}"


class CartOrder(models.Model):
    PAYMENT_STATUS = (
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("canceled", "Canceled"),
    )
    ORDER_STATUS = (
        ("Pending", "Pending"),
        ("Fulfilled", "Fulfilled"),
        ("Canceled", "Canceled"),
    )
    vendor = models.ManyToManyField(Vendor, blank=True)
    buyer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    sub_total = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    service_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    payment_status = models.CharField(
        max_length=100, choices=PAYMENT_STATUS, default="pending")
    order_status = models.CharField(
        max_length=100, choices=ORDER_STATUS, default="pending")

    # Coupons
    initial_total = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    saved = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    # Bio Data
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)

    # Shipping Address
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    oid = ShortUUIDField(unique=True, length=10, alphabet="abcdefg12345")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oid


class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    sub_total = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    service_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    country = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)

    # Coupons
    initial_total = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    saved = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    oid = ShortUUIDField(unique=True, length=10, alphabet="abcdefg12345")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oid


class ProductFaq(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    question = models.CharField(max_length=1000)
    answer = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Products FAQs"


class Review(models.Model):
    RATING = (
        (1, "1 star"),
        (2, "2 star"),
        (3, "3 star"),
        (4, "4 star"),
        (5, "5 star"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    replay = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=None, choices=RATING)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name_plural = "Reviews & Rating"

    def profile(self):
        return Profile.objects.get(user=self.user)


@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    if instance.product:
        instance.product.save()


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(
        CartOrder, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(
        CartOrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.order:
            return self.order.oid
        else:
            return f"Notification - {self.pk}"


class Coupon(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    user_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=1000)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class Tax(models.Model):
    country = models.CharField(max_length=100)
    rate = models.IntegerField(
        default=5, help_text="Numbers added  here are in percentage e.g 5%")
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name_plural = "Taxes"
        ordering = ['country']
