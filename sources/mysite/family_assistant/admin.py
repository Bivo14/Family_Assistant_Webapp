from django.contrib import admin
from .models import Parent, Child, External, Image, myUser, ImageComment, Child_Item, Measurement, Event 


# Register your models here.
admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(External)
admin.site.register(myUser)
admin.site.register(Image)
admin.site.register(ImageComment)
admin.site.register(Child_Item)
admin.site.register(Measurement)
admin.site.register(Event)