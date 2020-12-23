# importing necessery django classes 
from django.contrib.auth.models import User
from django.utils import timezone 
from django.db import models 
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
  
class myUser(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 200, null = True)
    profile_picture = models.ImageField(default = "avatars/profile1.png", upload_to = 'avatars', null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    class Meta:
        permissions = (
            ("view_home_page", "Permission to view the home page"),
            ("view_profile_page", "Permission to view the profile page"),
        )

    def __str__(self):
        return str(self.name)

class Parent(models.Model):
    user = models.OneToOneField(myUser, null = True, on_delete = models.CASCADE)

    class Meta:
        permissions = (
            ("view_travel_page", "Permission to view the travel page"),
            ("view_schedule_page", "Permission to view the schedule page"),
            ("view_memories_page", "Permission to view the memories page"),
            ("view_home_page", "Permission to view the home page"),
            ("view_profile_page", "Permission to view the profile page"),
        )

class Child(models.Model):
    user = models.OneToOneField(myUser, null = True, on_delete = models.CASCADE)

    class Meta:
        permissions = (
            ("view_travel_page", "Permission to view the travel page"),
            ("view_schedule_page", "Permission to view the schedule page"),
            ("view_memories_page", "Permission to view the memories page"),
            ("view_home_page", "Permission to view the home page"),
            ("view_profile_page", "Permission to view the profile page"),
        )

    def __str__(self):
        return self.user.name

class External(models.Model):
    user = models.OneToOneField(myUser, null = True, on_delete = models.CASCADE)

    class Meta:
        permissions = (
            ("view_schedule_page", "Permission to view the schedule page"),
            ("view_home_page", "Permission to view the home page"),
            ("view_profile_page", "Permission to view the profile page"),
        )

    def __str__(self):
        return self.user.name

class Image(models.Model):
    title = models.CharField(max_length = 200, null = True)
    description = models.CharField(max_length = 200, null = True)
    image = models.ImageField(upload_to='images', null = True)

    def __str__(self):
        return self.title

class ImageComment(models.Model):
    author = models.ForeignKey(myUser, default = 1, on_delete = models.CASCADE)
    image = models.ForeignKey(Image, default = 1, on_delete = models.CASCADE)
    text = models.TextField(null = True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return self.text

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        myUser.objects.create(user = instance)
        group = Group.objects.get(name = 'Basic user')
        instance.groups.add(group)

post_save.connect(create_profile, sender = User)

class Child_Item(models.Model):
    CATEGORY = (
        ('Book', 'Book'),
        ('Movie', 'Movie'),
        ('Toy', 'Toy'),
        ('Clothes', 'Clothes'),
    )

    owner = models.ForeignKey(myUser, null = True, default = None, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, null = True)
    description = models.CharField(max_length = 200, null = True)
    category = models.CharField(max_length = 200, null = True, choices = CATEGORY)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Distance from {self.location} to {self.destination} is {self.distance} km"

class Event(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'