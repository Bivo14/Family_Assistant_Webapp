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

    def __str__(self):
        return str(self.name)

class Parent(models.Model):
    user = models.OneToOneField(myUser, null = True, on_delete = models.CASCADE)

    class Meta:
        permissions = (
            ('can_view_the_travel_page', "Access travel page"),
            ('can_view_schedule_page', "Access schedule page"),
        )

    def __str__(self):
        return self.user.name

class Child(models.Model):
    user = models.OneToOneField(myUser, null = True, on_delete = models.CASCADE)

    class Meta:
        permissions = (
            ('can_view_the_travel_page', "Access travel page"),
        )

    def __str__(self):
        return self.user.name

class External(models.Model):
    user = models.OneToOneField(myUser, null = True, on_delete = models.CASCADE)

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
        ('To read', 'To read'),
        ('To watch', 'To watch'),
        ('To buy', 'To buy'),
        ('To do', 'To do'),
    )

    STATUS = (
        ('Task done', 'Task done'),
        ('Task not done yet', 'Task not done yet'),
    )

    owner = models.ForeignKey(myUser, null = True, default = None, on_delete = models.CASCADE)
    name = models.CharField(max_length = 200, null = True)
    description = models.CharField(max_length = 200, null = True)
    category = models.CharField(max_length = 200, null = True, choices = CATEGORY)
    status = models.CharField(max_length = 200, null = True, choices = STATUS)

    def __str__(self):
        return self.name

class Personal_Event(models.Model):
    STATUS = (
        ('Task done', 'Task done'),
        ('Task not done yet', 'Task not done yet'),
    )

    person = models.ForeignKey(myUser, null = True, default = None, on_delete = models.CASCADE)
    task = models.CharField(max_length = 200, null = True)
    description = models.CharField(max_length = 200, null = True)
    start_time = models.DateTimeField(null = True)
    end_time = models.DateTimeField(null = True)
    status = models.CharField(max_length = 200, null = True, choices = STATUS, default = 'Task not done yet')

    def __str__(self):
        return self.task

class Measurement(models.Model):

    CATEGORY = (
        ('Approved', 'Approved'),
        ('Awaiting approval', 'Awaiting approval'),
    )

    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null = True)
    end_time = models.DateTimeField(null = True)

    votes = models.ManyToManyField(User, related_name = 'trip_vote')
    status = models.CharField(max_length = 200, null = True, choices = CATEGORY, default = 'Awaiting approval')
    

    def total_votes(self):
        return self.likes.count()


    def __str__(self):
        return f"Distance from {self.location} to {self.destination} is {self.distance} km"

class Event(models.Model):

    CATEGORY = (
        ('Urgent', 'Urgent'),
        ('Important', 'Important'),
        ('Can be delayed', 'Can be delayed'),
        ('Unimportant', 'Unimportant'),
    )

    title = models.CharField(max_length=200, null=True)
    person_in_charge = models.ForeignKey(myUser, null = True, default = None, on_delete = models.CASCADE)
    description = models.TextField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    importance = models.CharField(max_length=200, null=True, choices = CATEGORY)

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        if self.importance == "Important":
            return f'<a href="{url}" style="color:#EB0C2E; font-weight:bold; text-decoration: none;"> {self.title} - {self.person_in_charge.name}</a>'
        if self.importance == "Urgent":
            return f'<a href="{url}" style="color:#D90A9D; font-weight:bold; text-decoration: none;"> {self.title} - {self.person_in_charge.name}</a>'
        if self.importance == "Can be delayed":
            return f'<a href="{url}" style="color:#46791E; font-weight:bold; text-decoration: none;"> {self.title} - {self.person_in_charge.name}</a>'
        if self.importance == "Unimportant":
            return f'<a href="{url}" style="color:#1C15DC; font-weight:bold; text-decoration: none;"> {self.title} - {self.person_in_charge.name}</a>'
