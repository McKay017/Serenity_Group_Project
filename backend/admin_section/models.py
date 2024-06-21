from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique category names

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contents = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    RELATIONSHIP_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    dob = models.DateField()
    national_id = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    occupation = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    relationship_status = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    phone_number = models.CharField(max_length=15)
    agreed_to_rules = models.BooleanField(default=False)
    agreed_to_waiver = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    

class Waiter(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=15)
    home_address = models.TextField()
    email = models.EmailField(unique=True)
    waiter_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.full_name
    

# models.py


class ImageUpload(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class Room(models.Model):
    room_name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=100)
    image = models.ImageField(upload_to='room_images/')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.room_name

from django.core.exceptions import ValidationError
from django.utils import timezone
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date < timezone.now().date():
            raise ValidationError('Start date cannot be in the past.')
        if self.end_date < self.start_date:
            raise ValidationError('End date cannot be before start date.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate model fields
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member_name} - {self.room.name} ({self.start_date} to {self.end_date})"
    

# payments/models.py

from django.db import models

class MpesaTransaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount}"


# membership/models.py

from django.db import models

class Membership(models.Model):
    MEMBERSHIP_TYPES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]

    user_id = models.IntegerField(unique=True)
    phone_number = models.CharField(max_length=15)
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_TYPES)

    def __str__(self):
        return f"User {self.user_id} - Type: {self.get_membership_type_display()}"

    def get_amount(self):
        if self.membership_type == 'basic':
            return 1.0
        elif self.membership_type == 'premium':
            return 2.0
        elif self.membership_type == 'vip':
            return 3.0
        return 0.0


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name