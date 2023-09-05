from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class VideoIdForm(forms.Form):
    video_id = forms.CharField(label="Video ID", max_length=100)
    
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class audioAccept(forms.Form):
    audioFile = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg'])])
        
