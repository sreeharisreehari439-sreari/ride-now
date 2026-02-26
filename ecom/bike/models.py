from django.db import models
from django.contrib.auth.models import User


# --------------------------------
# CATEGORY MODEL
# --------------------------------
class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name



class Bike(models.Model):

    CONDITION_CHOICES = (
        ('new', 'New'),
        ('used', 'Used'),
    )

    FUEL_CHOICES = (
        ('petrol', 'Petrol'),
        ('electric', 'Electric'),
        ('diesel', 'Diesel'),
    )

    # Seller
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bikes"
    )

    # Basic Details
    title = models.CharField(max_length=200)

    brand = models.CharField(max_length=100)

    # Category Relation
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bikes"
    )

    description = models.TextField()

    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        default='new'
    )

    # Specifications
    year = models.PositiveIntegerField()

    mileage = models.PositiveIntegerField(
        help_text="KM Driven"
    )

    engine_capacity = models.CharField(
        max_length=50,
        help_text="Example: 150cc"
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
        default='petrol'
    )

    color = models.CharField(max_length=50)

    location = models.CharField(max_length=200)

    # MAIN IMAGE (Primary Thumbnail)
    main_image = models.ImageField(
        upload_to="bike_images/"
    )

    # Inventory
    stock = models.PositiveIntegerField(default=1)

    is_available = models.BooleanField(default=True)

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.title


# --------------------------------
# ORDER MODEL
# --------------------------------
class Order(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    quantity = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    ordered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.bike.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.bike.title}"


