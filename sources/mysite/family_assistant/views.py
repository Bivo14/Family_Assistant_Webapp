from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.views import generic
from django.utils.safestring import mark_safe

from datetime import datetime, timedelta, date
from calendar import HTMLCalendar

from .models import *
from .forms import *
from .utils import *
from .group_check import group_required

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
import calendar

# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        context = {'form':form}
        return render(request, 'base_templates/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {}
        return render(request, 'base_templates/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required
@group_required('Parent', 'Child', 'External', 'Basic user')
def accountSettings(request):
    get_user = request.user.myuser
    form = UserForm(instance = get_user)
    form.fields['user'].widget = forms.HiddenInput()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = get_user)
        if form.is_valid():
            my_group = Group.objects.get(name = str(form['group'].value()))
            my_group.user_set.add(form['user'].value())
            form.save()
    context = {'form':form, 'user':get_user}
    return render(request, 'base_templates/user_page.html', context)


@login_required
@group_required('Parent', 'Child', 'External', 'Basic user')
def homePage(request):
    print (request.user.id)
    return render(request, 'base_templates/homepage.html')

@login_required
@group_required('Parent', 'Child')
def memoriesPage(request):
    images = Image.objects.all()
    return render(request, 'memories_templates/memories.html', {'images':images})

@login_required
@group_required('Parent', 'Child')
def travelPage(request):
    return render(request, 'travel.html')
        

@login_required
@group_required('Parent', 'Child', 'External')
def schedulePage(request):
    return render(request, 'calendar_templates/schedule.html')


######## PAGINA AMINTIRI ##########


@login_required
@group_required('Parent', 'Child')
def uploadImage(request):
    if request.method == "POST":
        form = CreateImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_object = form.instance
            return render(request, "memories_templates/upload_memory.html", {'form':form, 'img_object':img_object})
    else:
        form = CreateImageForm()
    return render(request, 'memories_templates/upload_memory.html', {'form':form})

@login_required
@group_required('Parent', 'Child')
def removeImage(request, pk):
    image = Image.objects.get(id = pk)
    if request.method == 'POST':
        image.delete()
        return redirect('/')
    context = {'item':image}
    return render(request, 'memories_templates/delete_memory.html', context)

@login_required
@group_required('Parent', 'Child')
def updateMemory(request, pk):
    get_image = Image.objects.get(id = pk)
    form = CreateImageForm(instance = get_image)
    if request.method == 'POST':
        form = CreateImageForm(request.POST, request.FILES, instance = get_image)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'memories_templates/modify_memory.html', context)

@login_required
@group_required('Parent', 'Child')
def addComment(request, pk):
    comments = ImageComment.objects.all()
    get_image = Image.objects.get(id = pk)
    get_user = request.user
    author = myUser.objects.get(user = get_user) 
    form = AddCommentForm(request.POST)
    if request.method == 'POST':
        text = form['text'].value()
        new_comment = ImageComment.objects.create(author = author, image = get_image, text = text)
        form = AddCommentForm(request.POST, request.FILES, instance = new_comment)
        if form.is_valid():
            form.save()            
            return redirect(request.path_info)
    image_comments = ImageComment.objects.all()
    context = {'form':form, 'image':get_image, 'comments':image_comments}
    return render(request, 'memories_templates/add_comment.html', context)


####################

@login_required
@group_required('Parent', 'Child', 'External')
def addPersonalEvent(request, pk):
    user_to_get = request.user 
    get_user = myUser.objects.get(user = user_to_get)
    personal_events = Personal_Event.objects.all()
    form = AddPersonalEventForm(request.POST)
    if request.method == 'POST':
        task = form['task'].value()
        description = form['description'].value()
        start_time = form['start_time'].value()
        end_time = form['end_time'].value()
        new_event = personal_events.create(person = get_user, task = task, description = description, start_time = start_time, end_time = end_time)
        form = AddPersonalEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    personal_events = Personal_Event.objects.all()
    context = {'form':form, 'personal_events':personal_events}
    return render(request, 'lists_templates/add_personal_event.html', context)

@login_required
@group_required('Parent', 'Child', 'External')
def viewPersonalEvents(request, pk):
    user_to_get = request.user
    get_user = myUser.objects.get(user = user_to_get)
    items = Personal_Event.objects.all()
    return render(request, 'lists_templates/render_events.html', {'user':get_user, 'personal_events':items})

@login_required
@group_required('Parent', 'Child', 'External')
def removePersonalEvent(request, pk):
    item = Personal_Event.objects.get(id = pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'personal_event':item}
    return render(request, 'lists_templates/delete_personal_event.html', context)
        
@login_required 
@group_required('Parent', 'Child', 'External')
def checkPersonalEvent(request, pk):
    post = get_object_or_404(Personal_Event, id=request.POST.get('tick_task'))
    if request.method == 'POST':
        if post.status != 'Task done':
            post.status = 'Task done'
            post.save()
        else:
            post.status = 'Task not done yet'
            post.save()
    return HttpResponseRedirect(reverse('viewPersonalEvents', args=[str(pk)]))  



####### PERSONAL LISTS #########

@login_required
@group_required('Parent', 'Child')
def addItem(request, pk):
    user_to_get = request.user
    get_user = myUser.objects.get(user = user_to_get)
    child_objects = Child_Item.objects.all()
    form = AddChildItemForm(request.POST)
    if request.method == 'POST':
        name = form['name'].value()
        description = form['description'].value()
        category = form['category'].value()
        new_object = child_objects.create(owner = get_user, name = name, description = description, category = category)
        form = AddChildItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    child_objects = Child_Item.objects.all()
    context = {'form':form, 'child_objects':child_objects}
    return render(request, 'lists_templates/add_child_item.html', context)

@login_required
@group_required('Parent', 'Child')
def viewItems(request, pk):
    user_to_get = request.user
    get_user = myUser.objects.get(user = user_to_get)
    items = Child_Item.objects.all()
    return render(request, 'lists_templates/render_items.html', {'user':get_user, 'items':items})

@login_required
@group_required('Parent', 'Child')
def removeItem(request, pk):
    item = Child_Item.objects.get(id = pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'item':item}
    return render(request, 'lists_templates/delete_item.html', context)

@login_required 
@group_required('Parent', 'Child')
def checkItem(request, pk):
    post = get_object_or_404(Child_Item, id=request.POST.get('tick_button'))
    if request.method == 'POST':
        if post.status != 'Task done':
            post.status = 'Task done'
            post.save()
        else:
            post.status = 'Task not done yet'
            post.save()
    return HttpResponseRedirect(reverse('viewLists', args=[str(pk)]))  

####################

######### TRAVEL PAGE ###########

@login_required
@group_required('Parent', 'Child')
def calculate_distance_view(request):

    # initial values
    distance = None
    destination = None
    
    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='family_assistant')

    # initial folium map
    m = folium.Map(width=800, height=500, zoom_start=1)

    if form.is_valid():
        instance = form.save(commit=False)

        location_ = form.cleaned_data.get('location')
        location = geolocator.geocode(location_)
        l_lat = location.latitude 
        l_lon = location.longitude
        pointA = (l_lat, l_lon)

        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)

        # destination coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)
        # distance calculation
        distance = round(geodesic(pointA, pointB).km, 2)

        # folium map modification
        m = folium.Map(width=800, height=500, location=get_center_coordinates(l_lat, l_lon, d_lat, d_lon), zoom_start=get_zoom(distance))
        # location marker
        folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=location,
                    icon=folium.Icon(color='purple')).add_to(m)
        # destination marker
        folium.Marker([d_lat, d_lon], tooltip='click here for more', popup=destination,
                    icon=folium.Icon(color='red', icon='cloud')).add_to(m)


        # draw the line between location and destination
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        m.add_child(line)

        instance.location = location
        instance.distance = distance
        instance.save()

        #m.save(str(instance.id) + ".html")
        
    
    m = m._repr_html_()

    travels = Measurement.objects.all()

    context = {
        'distance' : distance,
        'destination': destination,
        'form': form,
        'map': m,
        'travels':travels,
    }

    return render(request, 'travel_templates/travel_add.html', context)

@login_required
@group_required('Parent')
def removeTravel(request, pk):
    travel = Measurement.objects.get(id = pk)
    if request.method == 'POST':
        travel.delete()
        return redirect('/')
    context = {'travel':travel}
    return render(request, 'travel_templates/travel_delete.html', context)

@login_required
@group_required('Parent', 'Child')
def VoteView(request, pk):
    post = get_object_or_404(Measurement, id=request.POST.get('vote_button'))
    post.votes.add(request.user)
    return HttpResponseRedirect(reverse('travel'))

@login_required
@group_required('Parent', 'Child')
def UnVoteView(request, pk):
    post = get_object_or_404(Measurement, id=request.POST.get('unvote_button'))
    post.votes.remove(request.user)
    return HttpResponseRedirect(reverse('travel'))

@login_required
@group_required('Parent')
def approveTravel(request, pk):
    post = get_object_or_404(Measurement, id=request.POST.get('approve_button'))
    if request.method == 'POST':
        if post.status != 'Approved':
            post.status = 'Approved'
            post.save()
        else:
            post.status = 'Awaiting approval'
            post.save()
    return HttpResponseRedirect(reverse('travel'))    


####################

##### calendar #####

class CalendarView(generic.ListView):
    model = Event
    template_name = 'calendar_templates/schedule.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

@login_required
@group_required('Parent', 'Child', 'External')
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('schedule'))
    return render(request, 'calendar_templates/events.html', {'form': form})

####################

    


