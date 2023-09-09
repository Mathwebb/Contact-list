from typing import Any
from contact.models import Contact
from django.core.exceptions import ValidationError

from django import forms

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        )
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