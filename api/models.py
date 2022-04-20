from django.db import models
from django.contrib.auth.models import User


ROLE_TYPE_CHOICES = (
    ('brand', 'Brand'), ('influencer', 'Influencer')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=100, null=True, blank=True)
    dob = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=12, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    hometown = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    role_type = models.CharField(max_length=50, choices=ROLE_TYPE_CHOICES, default='influencer')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'


class Page(models.Model):
    page_uid = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    about = models.CharField(max_length=500, blank=True, null=True)
    page_token = models.CharField(max_length=500, blank=True, null=True)
    page_picture = models.CharField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    followers = models.IntegerField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    fans = models.IntegerField(null=True, blank=True)
    has_whatsapp_number = models.BooleanField(default=False)
    whatsapp_number = models.CharField(max_length=50, blank=True, null=True)
    page_link = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.page_uid}-{self.name}-{self.profile}'

