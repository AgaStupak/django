from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Aukcja, Komentarz, PodKategoria

class AukcjaForm(forms.ModelForm):
    class Meta:
        model = Aukcja
        fields = ('title', 'text','kategoria', 'podkategoria', 'zdjecie')

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('first_name', 'last_name', 'email')

class KomentarzForm(forms.ModelForm):

    class Meta:
        model = Komentarz
        fields = ('text',)

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = PodKategoria
        fields = ('kategoria', 'podkategoria')