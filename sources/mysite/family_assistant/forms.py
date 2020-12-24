from django.forms import ModelForm, DateInput
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django import forms 
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserForm(ModelForm):
	class Meta:
		model = myUser
		fields = '__all__'
		exclude = ['user']

class CreateImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image', 'description']

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = ImageComment
        fields = '__all__'
        exclude = ['author', 'image', 'date_created']

class AddChildItemForm(forms.ModelForm):
    class Meta:
        model = Child_Item
        fields = ['name', 'description', 'category']

class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model = Measurement
        widgets = {
          'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
          'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ('location', 'destination', 'start_time', 'end_time')

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

