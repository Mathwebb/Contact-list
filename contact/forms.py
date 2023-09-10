from typing import Any
from contact.models import Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from django import forms

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        ),
        required=False
    )

    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category',
            'picture',
        )
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = self.cleaned_data
        return super().clean()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3
    )

    last_name = forms.CharField(
        required=True,
        min_length=3
    )

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    'Este endereço de email já está sendo utilizado.',
                    code='invalid'
                )
            )

        return email


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please add more than two characters'
        }
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please add more than two characters'
        }
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label='Confirm password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Confirm your password',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user =  super().save(commit=False)
        
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()
        
        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            self.add_error(
                'password2',
                ValidationError('As senhas devem ser iguais.')
            )

        return super().clean()

            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if email != current_email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        'Este endereço de email já está sendo utilizado.',
                        code='invalid'
                    )
                )

        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1
