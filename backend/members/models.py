

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Proposed(models.Model):
    proposed_email = models.EmailField()
    seconder_userid = models.CharField(max_length=100,null=True)
    seconder_email = models.EmailField()
    name = models.CharField(max_length=255,null=True)
    id_number = models.CharField(max_length=100,null=True)
    occupation = models.CharField(max_length=100,null=True)
    employer = models.CharField(max_length=100,null=True)
    relationship_status = models.CharField(max_length=50,null=True)
    children = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=20,null=True)
    salary_range = models.CharField(max_length=100,null=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    email = models.EmailField(null=True)
    def __str__(self):
        return self.proposed_email

class Accepted(models.Model):
    proposed_email = models.EmailField()
    seconder_userid = models.CharField(max_length=100)
    seconder_email = models.EmailField()
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    relationship_status = models.CharField(max_length=50)
    children = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    salary_range = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    def __str__(self):
        return f"Accepted request for {self.proposed_email} by {self.user.username}"  # Example format


class Rejected(models.Model):
    proposed_email = models.EmailField()
    seconder_userid = models.CharField(max_length=100)
    seconder_email = models.EmailField()
    name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    relationship_status = models.CharField(max_length=50)
    children = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    salary_range = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    def __str__(self):
        return f"Rejected request for {self.proposed_email} by {self.user.username}"  # Example format
