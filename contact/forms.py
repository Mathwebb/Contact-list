from typing import Any
from contact.models import Contact

from django import forms

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone',)
    
    def clean(self) -> dict[str, Any]:
        return super().clean()