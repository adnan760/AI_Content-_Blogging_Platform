from django.db import models
from django.template.defaultfilters import slugify
from django_resized import ResizedImageField
from django.utils import timezone
# from django.urls import reverse
from uuid import uuid4
import os
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    SUBSCRIPTION_OPTIONS = [
        ('free', 'free'),
        ('starter', 'starter'),
        ('advanced', 'advanced')
    ]

    #Standard Variables
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addressLine1 = models.CharField(null=True, blank=True, max_length=100)
    addressLine2 = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=100)
    state = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
    postalCode = models.CharField(null=True, blank=True, max_length=100)
    profileImage = ResizedImageField(size=[100,100],quality=75,upload_to="profile_image")

    monthlyCount = models.CharField(null=True, blank=True, max_length=100)
    subscribed = models.BooleanField(default=False)
    subscriptionType = models.CharField(choices=SUBSCRIPTION_OPTIONS, default='free', max_length=100)
    subscriptionReference = models.CharField(null=True, blank=True, max_length=100)
    subscriptionDate = models.DateTimeField(blank=True, null=True)

    #Utility Variable
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.user.first_name,self.user.last_name,self.user.email)


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]


        self.slug = slugify('{} {} {}'.format(self.user.first_name,self.user.last_name,self.user.email))
        self.last_updated = timezone.localtime(timezone.now())
        super(Profile, self).save(*args, **kwargs)



class Blog(models.Model):
    title = models.CharField(max_length=200)
    blogIdea = models.CharField(null=True, blank=True, max_length=200)
    keywords = models.CharField(null=True, blank=True, max_length=300)
    audience = models.CharField(null=True, blank=True, max_length=100)
    wordCount = models.CharField(null=True, blank=True, max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    #Utility Variable
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.title, self.uniqueId)


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.slug = slugify('{} {}'.format(self.title, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(Blog, self).save(*args, **kwargs)


class BlogSection(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    wordCount = models.CharField(null=True, blank=True, max_length=200)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    #Utility Variable
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.title, self.uniqueId)


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]


        self.slug = slugify('{} {}'.format(self.title, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        if self.body:
            x = len(self.body.split(' '))
            self.wordCount = str(x)
        super(BlogSection, self).save(*args, **kwargs)