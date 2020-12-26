from django.contrib import admin
from .models import *
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Permission

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
admin.site.register(Permission)
admin.site.register(Personal_Event)



