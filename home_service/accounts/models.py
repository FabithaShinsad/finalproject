from django.contrib.auth.models import AbstractUser
from django.db import models
from services.models import Service
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username
class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    services = models.ManyToManyField('services.Service', blank=True)

    skill = models.CharField(max_length=100, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    profile_image = models.ImageField(upload_to='freelancers/', null=True, blank=True)

    def __str__(self):
        return self.user.username
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    profile_image = models.ImageField(upload_to='clients/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    def __str__(self):
        return self.user.username    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'freelancer':
            FreelancerProfile.objects.create(user=instance)
        elif instance.user_type == 'client':
            ClientProfile.objects.create(user=instance)    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message            
