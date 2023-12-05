from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Manager para nuestro CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_super_user', True)
        return self.create_user(email, password, **extra_fields)

# Modelo CustomUser
class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255, blank=True)
    lastname_m = models.CharField(max_length=255, blank=True)
    is_super_user = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.username

# Modelo LoginAttempt
class LoginAttempt(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


# Modelo Trade
class Trade(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='initiated')
    date_initiated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    initiator = models.ForeignKey(CustomUser, related_name='initiated_trades', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='receiver_trades', on_delete=models.CASCADE, null=True, blank=True)
    initiator_item = models.ForeignKey('Item', related_name='trades_as_initiator', on_delete=models.SET_NULL, null=True)
    responder_item = models.ForeignKey('Item', related_name='trades_as_responder', on_delete=models.SET_NULL, null=True)

# Modelo UserTrade
class UserTrade(models.Model):
    custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (('custom_user', 'trade'),)

# Modelo Item
class Item(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='item_images/')