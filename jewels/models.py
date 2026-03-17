from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
class CustomUser(AbstractUser):
    mobile = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Mobile number must be 10 digits')]
    )
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email or str(self.mobile)


class Rate(models.Model):
    RATE_TYPE_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
    ]
    
    rate_type = models.CharField(max_length=10, choices=RATE_TYPE_CHOICES)
    per_gram_rate = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    class Meta:
        unique_together = ['rate_type', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.rate_type.capitalize()} - {self.per_gram_rate} per gram ({self.date})"


class Item(models.Model):
    ITEM_TYPE_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
    ]

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='items/')
    #video_file = models.FileField(upload_to='videos/')
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True, help_text='Additional details about the item')
    video_url = models.URLField(blank=True, null=True, help_text='Optional video URL (YouTube, etc.)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def calculate_price(self):
        """Calculate price based on current rate"""
        try:
            current_rate = Rate.objects.filter(
                rate_type=self.item_type
            ).order_by('-date').first()
            if current_rate:
                return self.weight * current_rate.per_gram_rate
            return 0
        except:
            return 0
    
    def save(self, *args, **kwargs):
        # Auto-calculate price before saving
        calculated_price = self.calculate_price()
        if calculated_price > 0:
            self.price = calculated_price
        super().save(*args, **kwargs)
    
    def video_embed_url(self):
        """Convert YouTube watch URL to embed URL for iframe."""
        if not self.video_url:
            return None
        import re
        url = self.video_url
        if 'youtube.com/watch' in url:
            m = re.search(r'v=([^&]+)', url)
            if m:
                return 'https://www.youtube.com/embed/' + m.group(1)
        if 'youtu.be/' in url:
            m = re.search(r'youtu\.be/([^?]+)', url)
            if m:
                return 'https://www.youtube.com/embed/' + m.group(1)
        return url

    def __str__(self):
        return f"{self.name} ({self.item_type})"


class ItemImage(models.Model):
    """Additional images for an item."""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='items/extras/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.item.name}"


# class Cart(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'item']
    
#     def __str__(self):
#         return f"{self.user.username} - {self.item.name}"
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'item']

    def total_price(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    payment_method = models.CharField(max_length=20, default='cash_on_delivery')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.order.id} - {self.item.name}"
