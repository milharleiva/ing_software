from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
import re
from django.contrib.auth.models import User

from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'disponible']

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        validators=[RegexValidator(
            regex=r'^[\w.-]+\Z', 
            message="This value may contain only letters, numbers, and ./-/_ characters.",
            flags=re.ASCII
        )]
    )

    class Meta:
        model = User
        fields = ("username",)
