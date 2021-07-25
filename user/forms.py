from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile


class UserRegistrationForm(UserCreationForm):
	"""
	Form for the user registration.
	:model : 'auth.user'
	"""
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def clean(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get("username")
		if User.objects.filter(username=username).exists():
			raise ValidationError("Username already taken!")
		if "@gmail.com" not in email:
			raise ValidationError("Only google accounts are accepted!")
		if User.objects.filter(email=email).exists():
			raise ValidationError("Email entered already used!")
		return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
	"""
	Form for the user edit.
	:model : 'auth.user'
	"""
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
	"""
	Form for the profile update of the user.
	:model : 'auth.user.profile'
	"""
	class Meta:
		model = Profile
		fields = ["image", "fullname", "status", "address", "bio"]
