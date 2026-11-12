from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class", default="fa-box")

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Location(models.Model):
    """Specific areas within Dormaa Ahenkro & surroundings"""
    name = models.CharField(max_length=100)  # e.g., Tuesday Market, VIP Station, Campus, Aboabo

    def __str__(self):
        return self.name


class ItemListing(models.Model):
    CONDITION_CHOICES = (
        ('NEW', 'Brand New'),
        ('FOREIGN_USED', 'Foreign Used (Home Used)'),
        ('LOCAL_USED', 'Locally Used'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('ACTIVE', 'Active'),
        ('SOLD', 'Sold'),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='listings')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_negotiable = models.BooleanField(default=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='LOCAL_USED')
    
    description = models.TextField()
    phone_number = models.CharField(max_length=15, help_text="MTN / Telecel contact number")
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Feature / Boost settings (Tonaton model)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - GHS {self.price}"


class ListingImage(models.Model):
    listing = models.ForeignKey(ItemListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/%Y/%m/%d/')
    is_primary = models.BooleanField(default=False)